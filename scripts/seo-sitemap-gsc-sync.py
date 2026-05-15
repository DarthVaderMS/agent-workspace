#!/usr/bin/env python3
"""
seo-sitemap-gsc-sync.py

Daily SEO visibility report for miguel.ms using the current Linux/gog setup.

Progress/logging goes to stderr. The final Discord payload is emitted to stdout
wrapped in <output>...</output> so the OpenClaw cron can relay only that content.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
SITE_BASE = "https://miguel.ms"
SITE_URL_PREFIX = "https://miguel.ms/"
SITE_DOMAIN = "sc-domain:miguel.ms"
SITEMAP_INDEX = f"{SITE_BASE}/sitemap-index.xml"
STATE_FILE = WORKSPACE / "memory/seo-sync-state.json"
REPORT_FILE = WORKSPACE / "memory/seo-sync-latest-report.txt"
GOG = "/home/linuxbrew/.linuxbrew/bin/gog"
GOG_ACCOUNT = "darth@miguel.ms"
USER_AGENT = "Mozilla/5.0 OpenClaw SEO Sync"
LOOKBACK_DAYS = 90
MAX_MISSING_TO_SHOW = 25


class SyncError(RuntimeError):
    pass


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def run_json(args: list[str]) -> dict[str, Any]:
    env = os.environ.copy()
    env["HOME"] = "/home/openclaw"
    cmd = [GOG, *args, "--account", GOG_ACCOUNT, "--json"]
    log(f"  → {' '.join(cmd)}")
    proc = subprocess.run(
        cmd,
        cwd=str(WORKSPACE),
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
    )
    if proc.returncode != 0:
        stderr = " ".join(proc.stderr.strip().split())
        stdout = " ".join(proc.stdout.strip().split())
        raise SyncError(stderr or stdout or f"gog exited {proc.returncode}")
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise SyncError(f"gog returned non-JSON output: {exc}") from exc


def fetch_xml(url: str) -> ET.Element:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return ET.fromstring(response.read())


def fetch_sitemap_urls(url: str) -> list[str]:
    urls: set[str] = set()
    root = fetch_xml(url)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    for sitemap in root.findall("sm:sitemap/sm:loc", ns):
        if sitemap.text:
            urls.update(fetch_sitemap_urls(sitemap.text.strip()))

    for entry in root.findall("sm:url/sm:loc", ns):
        if entry.text:
            loc = entry.text.strip()
            if loc == SITE_BASE:
                loc = SITE_URL_PREFIX
            urls.add(loc)

    return sorted(urls)


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"known_urls": [], "last_run": None}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception as exc:
        log(f"  ⚠ Could not parse {STATE_FILE}: {exc}; treating state as empty")
        return {"known_urls": [], "last_run": None}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def normalize_url(url: str) -> str:
    if url == SITE_BASE:
        return SITE_URL_PREFIX
    return url


def path_for(url: str) -> str:
    normalized = normalize_url(url)
    if normalized == SITE_URL_PREFIX:
        return "/"
    if normalized.startswith(SITE_BASE):
        return normalized[len(SITE_BASE) :] or "/"
    return normalized


def rows_from_query(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("rows")
    return rows if isinstance(rows, list) else []


def visible_pages_from_rows(rows: list[dict[str, Any]]) -> set[str]:
    pages: set[str] = set()
    for row in rows:
        keys = row.get("keys") or []
        if keys:
            pages.add(normalize_url(str(keys[0])))
    return pages


def get_searchconsole_rows(today: dt.date) -> tuple[str, list[dict[str, Any]]]:
    start = (today - dt.timedelta(days=LOOKBACK_DAYS)).isoformat()
    end = today.isoformat()

    prefix_payload = run_json(
        [
            "searchconsole",
            "query",
            SITE_URL_PREFIX,
            "--from",
            start,
            "--to",
            end,
            "--dimensions",
            "page",
            "--max",
            "25000",
        ]
    )
    prefix_rows = rows_from_query(prefix_payload)
    if prefix_rows:
        return SITE_URL_PREFIX, prefix_rows

    log("  → URL-prefix query returned no rows; falling back to domain property")
    domain_payload = run_json(
        [
            "searchconsole",
            "query",
            SITE_DOMAIN,
            "--from",
            start,
            "--to",
            end,
            "--dimensions",
            "page",
            "--max",
            "25000",
        ]
    )
    return SITE_DOMAIN, rows_from_query(domain_payload)


def sitemap_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("sitemaps")
    return rows if isinstance(rows, list) else []


def format_sitemap_row(row: dict[str, Any]) -> str:
    submitted = str(row.get("lastSubmitted") or "?")[:10]
    warnings = row.get("warnings", 0) or 0
    errors = row.get("errors", 0) or 0
    path = row.get("path", "?")
    return f"  • {path} (submitted: {submitted}, w={warnings}, e={errors})"


def build_report(
    today: dt.date,
    sitemap_urls: list[str],
    visible_pages: set[str],
    visibility_source: str,
    sitemaps: list[dict[str, Any]],
    new_urls: list[str],
    removed_urls: list[str],
) -> str:
    sitemap_set = set(sitemap_urls)
    visible_in_sitemap = sitemap_set & visible_pages
    missing = sorted(sitemap_set - visible_pages)

    lines = [
        f"📊 **SEO Daily Sync — {today.isoformat()}**",
        f"Site: <{SITE_BASE}> | {len(sitemap_urls)} URLs in sitemap | "
        f"✅ {len(visible_in_sitemap)} visible in GSC / ⚠️ {len(missing)} not seen in recent GSC page data",
        f"Visibility source: `{visibility_source}` over the last {LOOKBACK_DAYS} days",
        "",
    ]

    if sitemaps:
        lines.append(f"📥 **Sitemaps in GSC:** {len(sitemaps)}")
        lines.extend(format_sitemap_row(row) for row in sitemaps)
        lines.append("")

    if new_urls:
        lines.append(f"🆕 **{len(new_urls)} new URL(s) in sitemap:**")
        lines.extend(f"  • `{path_for(url)}`" for url in new_urls[:MAX_MISSING_TO_SHOW])
        if len(new_urls) > MAX_MISSING_TO_SHOW:
            lines.append(f"  • …and {len(new_urls) - MAX_MISSING_TO_SHOW} more")
        lines.append("")

    if removed_urls:
        lines.append(f"⚠️ **{len(removed_urls)} URL(s) removed from sitemap:**")
        lines.extend(f"  • `{path_for(url)}`" for url in removed_urls[:MAX_MISSING_TO_SHOW])
        if len(removed_urls) > MAX_MISSING_TO_SHOW:
            lines.append(f"  • …and {len(removed_urls) - MAX_MISSING_TO_SHOW} more")
        lines.append("")

    if missing:
        lines.append("📋 **Not seen in recent GSC page data:**")
        lines.extend(f"  • `{path_for(url)}`" for url in missing[:MAX_MISSING_TO_SHOW])
        if len(missing) > MAX_MISSING_TO_SHOW:
            lines.append(f"  • …and {len(missing) - MAX_MISSING_TO_SHOW} more")
        lines.append("")

    if not new_urls and not removed_urls and not missing:
        lines.append("No structural changes detected today.")

    return "\n".join(lines).strip()


def run_sync() -> str:
    today = dt.date.today()
    log(f"[{today.isoformat()}] SEO Sitemap ↔ GSC sync starting")

    log("  → Checking Search Console property")
    run_json(["searchconsole", "sites", "get", SITE_URL_PREFIX])

    log("  → Fetching sitemap URLs")
    sitemap_urls = fetch_sitemap_urls(SITEMAP_INDEX)
    log(f"  → {len(sitemap_urls)} URLs in sitemap")

    log("  → Reading GSC sitemaps")
    sitemaps_payload = run_json(["searchconsole", "sitemaps", "list", SITE_URL_PREFIX])
    sitemaps = sitemap_rows(sitemaps_payload)

    log("  → Reading Search Analytics page visibility")
    visibility_source, rows = get_searchconsole_rows(today)
    visible_pages = visible_pages_from_rows(rows)
    log(f"  → {len(visible_pages)} visible page row(s) from {visibility_source}")

    state = load_state()
    known_urls = {normalize_url(url) for url in state.get("known_urls", [])}
    sitemap_set = set(sitemap_urls)
    new_urls = sorted(sitemap_set - known_urls)
    removed_urls = sorted(known_urls - sitemap_set)

    report = build_report(
        today=today,
        sitemap_urls=sitemap_urls,
        visible_pages=visible_pages,
        visibility_source=visibility_source,
        sitemaps=sitemaps,
        new_urls=new_urls,
        removed_urls=removed_urls,
    )

    state.update(
        {
            "last_run": today.isoformat(),
            "known_urls": sitemap_urls,
            "visibility_source": visibility_source,
            "visible_pages": sorted(visible_pages),
        }
    )
    save_state(state)

    REPORT_FILE.write_text(report + "\n")
    log(f"  → Saved report to {REPORT_FILE}")
    return report


def main() -> int:
    try:
        report = run_sync()
    except Exception as exc:
        log(f"✗ SEO sync failed: {type(exc).__name__}: {exc}")
        return 1

    print("<output>")
    print(report)
    print("</output>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
