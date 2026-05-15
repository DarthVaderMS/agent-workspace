#!/usr/bin/env python3
"""
Weekly GA4/content report for miguel.ms using the current Linux/gog setup.

Operational logging goes to stderr. The final Discord payload is emitted to
stdout wrapped in <output>...</output> so the OpenClaw cron can relay only that
content.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
SNAPSHOT_DIR = WORKSPACE / "memory/seo-weekly"
LATEST_REPORT = WORKSPACE / "memory/seo-weekly-latest-report.txt"
GOG = "/home/linuxbrew/.linuxbrew/bin/gog"
GOG_ACCOUNT = "darth@miguel.ms"
GA4_PROPERTY = "properties/377775150"
SITE_BASE = "https://miguel.ms"
USER_AGENT = "Mozilla/5.0 OpenClaw Weekly Content Report"

TOP_LIMIT = 8


class ReportError(RuntimeError):
    pass


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def last_complete_week(today: dt.date | None = None) -> dict[str, dt.date]:
    today = today or dt.date.today()
    this_monday = today - dt.timedelta(days=today.weekday())
    current_start = this_monday - dt.timedelta(days=7)
    current_end = this_monday - dt.timedelta(days=1)
    previous_start = current_start - dt.timedelta(days=7)
    previous_end = current_start - dt.timedelta(days=1)
    return {
        "current_start": current_start,
        "current_end": current_end,
        "previous_start": previous_start,
        "previous_end": previous_end,
    }


def run_gog_report(
    start: dt.date,
    end: dt.date,
    dimensions: list[str],
    metrics: list[str],
    limit: int = 250,
) -> dict[str, Any]:
    env = os.environ.copy()
    env["HOME"] = "/home/openclaw"
    cmd = [
        GOG,
        "analytics",
        "report",
        GA4_PROPERTY,
        "--account",
        GOG_ACCOUNT,
        "--from",
        str(start),
        "--to",
        str(end),
        "--metrics",
        ",".join(metrics),
        "--max",
        str(limit),
        "--json",
        "--no-input",
    ]
    if dimensions:
        cmd.extend(["--dimensions", ",".join(dimensions)])
    log(f"  -> {' '.join(cmd)}")
    proc = subprocess.run(
        cmd,
        cwd=str(WORKSPACE),
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    if proc.returncode != 0:
        stderr = " ".join((proc.stderr or "").strip().split())
        stdout = " ".join((proc.stdout or "").strip().split())
        raise ReportError(stderr or stdout or f"gog exited {proc.returncode}")
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise ReportError(f"gog returned invalid JSON: {exc}") from exc


def metric(row: dict[str, Any], index: int) -> float:
    values = row.get("metricValues") or []
    if index >= len(values):
        return 0.0
    try:
        return float(values[index].get("value") or 0)
    except (TypeError, ValueError):
        return 0.0


def dimension(row: dict[str, Any], index: int) -> str:
    values = row.get("dimensionValues") or []
    if index >= len(values):
        return ""
    return str(values[index].get("value") or "")


def aggregate_rows(resp: dict[str, Any], dimensions: list[str], metrics: list[str]) -> dict[str, list[float]]:
    if not dimensions:
        totals = [0.0] * len(metrics)
        sessions_idx = metrics.index("sessions") if "sessions" in metrics else None
        engaged_idx = metrics.index("engagedSessions") if "engagedSessions" in metrics else None
        duration_weight = 0.0
        total_sessions = 0.0

        for row in resp.get("rows") or []:
            row_sessions = metric(row, sessions_idx) if sessions_idx is not None else 0.0
            total_sessions += row_sessions
            for idx, name in enumerate(metrics):
                value = metric(row, idx)
                if name == "averageSessionDuration":
                    duration_weight += value * row_sessions
                elif name == "engagementRate":
                    continue
                else:
                    totals[idx] += value

        if "averageSessionDuration" in metrics:
            idx = metrics.index("averageSessionDuration")
            totals[idx] = duration_weight / total_sessions if total_sessions else 0.0
        if "engagementRate" in metrics:
            idx = metrics.index("engagementRate")
            engaged = totals[engaged_idx] if engaged_idx is not None else 0.0
            sessions = totals[sessions_idx] if sessions_idx is not None else total_sessions
            totals[idx] = engaged / sessions if sessions else 0.0
        return {"__total__": totals}

    out: dict[str, list[float]] = {}
    for row in resp.get("rows") or []:
        if dimensions:
            key = " | ".join(dimension(row, idx) or "(not set)" for idx in range(len(dimensions)))
        else:
            key = "__total__"
        if key not in out:
            out[key] = [0.0] * len(metrics)
        for idx in range(len(metrics)):
            out[key][idx] += metric(row, idx)
    return out


def fetch_pair(
    ranges: dict[str, dt.date],
    dimensions: list[str],
    metrics: list[str],
    limit: int = 250,
) -> list[dict[str, Any]]:
    current = aggregate_rows(
        run_gog_report(ranges["current_start"], ranges["current_end"], dimensions, metrics, limit),
        dimensions,
        metrics,
    )
    previous = aggregate_rows(
        run_gog_report(ranges["previous_start"], ranges["previous_end"], dimensions, metrics, limit),
        dimensions,
        metrics,
    )
    keys = set(current) | set(previous)
    rows = []
    for key in keys:
        curr = current.get(key, [0.0] * len(metrics))
        prev = previous.get(key, [0.0] * len(metrics))
        rows.append({"key": key, "current": curr, "previous": prev})
    rows.sort(key=lambda row: row["current"][0], reverse=True)
    return rows


def pct_change(current: float, previous: float) -> float | None:
    if previous == 0:
        return None if current == 0 else float("inf")
    return ((current - previous) / previous) * 100.0


def fmt_change(current: float, previous: float) -> str:
    change = pct_change(current, previous)
    if change is None:
        return "0%"
    if change == float("inf"):
        return "+new"
    return f"{change:+.0f}%"


def trend(current: float, previous: float) -> str:
    if previous == 0 and current > 0:
        return "new"
    if current > previous:
        return "up"
    if current < previous:
        return "down"
    return "flat"


def fmt_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60}m{seconds % 60:02d}s"


def plural(value: float, singular: str, plural_form: str | None = None) -> str:
    word = singular if int(value) == 1 else (plural_form or f"{singular}s")
    return f"{int(value)} {word}"


def clean_path(path: str) -> str:
    if path == "(not set)":
        return path
    return path or "/"


def title_from_path(path: str) -> str:
    slug = path.rstrip("/").split("/")[-1] or "home"
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
    return slug.replace("-", " ").title()


def fetch_post_markdown(path: str) -> dict[str, str]:
    slug = path.rstrip("/").split("/")[-1]
    if not slug:
        return {"title": title_from_path(path), "excerpt": ""}
    url = f"{SITE_BASE}/blog/{slug}.md"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            text = response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            log(f"  WARN blog markdown fetch failed for {url}: HTTP {exc.code}")
        return {"title": title_from_path(path), "excerpt": ""}
    except Exception as exc:
        log(f"  WARN blog markdown fetch failed for {url}: {exc}")
        return {"title": title_from_path(path), "excerpt": ""}

    title = title_from_path(path)
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"') or title
            text = text[end + 5 :]
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip() or title
            break
    excerpt = " ".join(text.split())[:220]
    return {"title": title, "excerpt": excerpt}


def as_table_rows(rows: list[dict[str, Any]], metric_names: list[str]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = {"name": row["key"]}
        for idx, name in enumerate(metric_names):
            item[f"{name}_current"] = row["current"][idx]
            item[f"{name}_previous"] = row["previous"][idx]
        out.append(item)
    return out


def build_snapshot() -> dict[str, Any]:
    ranges = last_complete_week()
    log(f"Building weekly report for {ranges['current_start']} to {ranges['current_end']}")

    topline_metrics = [
        "sessions",
        "activeUsers",
        "screenPageViews",
        "engagedSessions",
        "engagementRate",
        "averageSessionDuration",
        "newUsers",
    ]
    topline_row = fetch_pair(ranges, [], topline_metrics, 10)[0]
    topline = {}
    for idx, name in enumerate(topline_metrics):
        topline[name] = {
            "current": topline_row["current"][idx],
            "previous": topline_row["previous"][idx],
        }

    channels = as_table_rows(
        fetch_pair(
            ranges,
            ["sessionDefaultChannelGroup"],
            ["sessions", "activeUsers", "engagedSessions", "engagementRate"],
            50,
        )[:TOP_LIMIT],
        ["sessions", "activeUsers", "engagedSessions", "engagementRate"],
    )
    sources = as_table_rows(
        fetch_pair(
            ranges,
            ["sessionSourceMedium"],
            ["sessions", "engagedSessions", "averageSessionDuration"],
            80,
        )[:TOP_LIMIT],
        ["sessions", "engagedSessions", "averageSessionDuration"],
    )
    utms = [
        row
        for row in as_table_rows(
            fetch_pair(
                ranges,
                ["sessionCampaignName", "sessionSource", "sessionMedium"],
                ["sessions", "engagedSessions", "engagementRate"],
                100,
            ),
            ["sessions", "engagedSessions", "engagementRate"],
        )
        if row["name"].split(" | ", 1)[0].lower() not in {"(not set)", "(organic)", "(direct)", "(referral)"}
    ][:TOP_LIMIT]
    landing_pages = as_table_rows(
        fetch_pair(
            ranges,
            ["landingPagePlusQueryString"],
            ["sessions", "engagedSessions", "activeUsers"],
            100,
        )[:TOP_LIMIT],
        ["sessions", "engagedSessions", "activeUsers"],
    )
    all_pages = as_table_rows(
        fetch_pair(
            ranges,
            ["pagePath"],
            ["sessions", "screenPageViews", "activeUsers", "averageSessionDuration"],
            250,
        ),
        ["sessions", "screenPageViews", "activeUsers", "averageSessionDuration"],
    )
    blog_posts = [row for row in all_pages if row["name"].startswith("/blog/")][:TOP_LIMIT]
    for post in blog_posts:
        context = fetch_post_markdown(post["name"])
        post["title"] = context["title"]
        post["excerpt"] = context["excerpt"]

    iso_year, iso_week, _ = ranges["current_start"].isocalendar()
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "week": {
            "current_start": str(ranges["current_start"]),
            "current_end": str(ranges["current_end"]),
            "previous_start": str(ranges["previous_start"]),
            "previous_end": str(ranges["previous_end"]),
            "iso_week": f"{iso_year}-W{iso_week:02d}",
        },
        "topline": topline,
        "channels": channels,
        "sources": sources,
        "utms": utms,
        "landing_pages": landing_pages,
        "blog_posts": blog_posts,
    }


def save_snapshot(snapshot: dict[str, Any]) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{snapshot['week']['iso_week']}.json"
    path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    return path


def best_and_drop(rows: list[dict[str, Any]], metric: str = "sessions") -> tuple[str | None, str | None]:
    growers = [
        row for row in rows
        if row.get(f"{metric}_current", 0) > row.get(f"{metric}_previous", 0)
    ]
    drops = [
        row for row in rows
        if row.get(f"{metric}_previous", 0) > row.get(f"{metric}_current", 0)
    ]
    growers.sort(key=lambda row: pct_change(row[f"{metric}_current"], row[f"{metric}_previous"]) or 0, reverse=True)
    drops.sort(key=lambda row: pct_change(row[f"{metric}_current"], row[f"{metric}_previous"]) or 0)
    return (
        growers[0]["name"] if growers else None,
        drops[0]["name"] if drops else None,
    )


def build_message(snapshot: dict[str, Any]) -> str:
    week = snapshot["week"]
    t = snapshot["topline"]
    channels = snapshot["channels"]
    sources = snapshot["sources"]
    utms = snapshot["utms"]
    landing_pages = snapshot["landing_pages"]
    blog_posts = snapshot["blog_posts"]

    best_channel, weak_channel = best_and_drop(channels)
    best_page, weak_page = best_and_drop(landing_pages)

    lines = [
        "**📈 Weekly Content Analysis Report — miguel.ms**",
        f"{week['current_start']} → {week['current_end']} vs {week['previous_start']} → {week['previous_end']}",
        "",
        "**Topline**",
        f"- **Sessions:** {int(t['sessions']['current'])} ({fmt_change(t['sessions']['current'], t['sessions']['previous'])})",
        f"- **Active users:** {int(t['activeUsers']['current'])} ({fmt_change(t['activeUsers']['current'], t['activeUsers']['previous'])})",
        f"- **Pageviews:** {int(t['screenPageViews']['current'])} ({fmt_change(t['screenPageViews']['current'], t['screenPageViews']['previous'])})",
        f"- **New users:** {int(t['newUsers']['current'])} ({fmt_change(t['newUsers']['current'], t['newUsers']['previous'])})",
        f"- **Engagement rate:** {t['engagementRate']['current'] * 100:.1f}% ({fmt_change(t['engagementRate']['current'], t['engagementRate']['previous'])})",
        f"- **Avg session duration:** {fmt_duration(t['averageSessionDuration']['current'])} ({fmt_change(t['averageSessionDuration']['current'], t['averageSessionDuration']['previous'])})",
        "",
        "**Channel signals**",
    ]
    if channels:
        for row in channels[:5]:
            lines.append(
                f"- **{row['name']}**: {plural(row['sessions_current'], 'session')} "
                f"({trend(row['sessions_current'], row['sessions_previous'])}, {fmt_change(row['sessions_current'], row['sessions_previous'])}); "
                f"ER {row['engagementRate_current'] * 100:.1f}%"
            )
    else:
        lines.append("- No channel data returned.")

    lines += ["", "**Source / medium**"]
    if sources:
        for row in sources[:5]:
            lines.append(
                f"- **{row['name']}**: {plural(row['sessions_current'], 'session')}; "
                f"{int(row['engagedSessions_current'])} engaged; avg {fmt_duration(row['averageSessionDuration_current'])}"
            )
    else:
        lines.append("- No source/medium data returned.")

    lines += ["", "**UTM signals**"]
    if utms:
        for row in utms[:5]:
            lines.append(
                f"- **{row['name']}**: {plural(row['sessions_current'], 'session')} "
                f"({fmt_change(row['sessions_current'], row['sessions_previous'])}); ER {row['engagementRate_current'] * 100:.1f}%"
            )
    else:
        lines.append("- No meaningful UTM-tagged traffic this week.")

    lines += ["", "**Top landing pages**"]
    if landing_pages:
        for row in landing_pages[:5]:
            lines.append(
                f"- `{clean_path(row['name'])}`: {plural(row['sessions_current'], 'session')} "
                f"({fmt_change(row['sessions_current'], row['sessions_previous'])})"
            )
    else:
        lines.append("- No landing-page data returned.")

    lines += ["", "**Top blog posts**"]
    if blog_posts:
        for post in blog_posts[:5]:
            title = post.get("title") or title_from_path(post["name"])
            lines.append(
                f"- **{title}**: {plural(post['sessions_current'], 'session')}, "
                f"{plural(post['screenPageViews_current'], 'view')}, avg {fmt_duration(post['averageSessionDuration_current'])} "
                f"({fmt_change(post['sessions_current'], post['sessions_previous'])})"
            )
    else:
        lines.append("- No blog-post traffic returned.")

    lines += ["", "**Read**"]
    if best_channel:
        lines.append(f"- Strongest channel movement: **{best_channel}**.")
    if weak_channel:
        lines.append(f"- Softest channel movement: **{weak_channel}**.")
    if best_page:
        lines.append(f"- Best landing-page movement: `{best_page}`.")
    if weak_page:
        lines.append(f"- Watch landing-page drop: `{weak_page}`.")
    if not any([best_channel, weak_channel, best_page, weak_page]):
        lines.append("- Traffic was stable or too thin for a clear movement read.")

    text = "\n".join(lines).strip()
    if len(text) > 5800:
        text = text[:5750].rsplit("\n", 1)[0] + "\n\n_Report trimmed for Discord length._"
    return text


def main() -> int:
    try:
        if not Path(GOG).exists():
            raise ReportError(f"gog binary not found at {GOG}")
        snapshot = build_snapshot()
        snapshot_path = save_snapshot(snapshot)
        message = build_message(snapshot)
        LATEST_REPORT.write_text(message + "\n")
        log(f"Saved weekly snapshot: {snapshot_path}")
        log(f"Saved latest report: {LATEST_REPORT}")
        print(f"<output>\n{message}\n</output>")
        return 0
    except Exception as exc:
        log(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
