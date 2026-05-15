#!/usr/bin/env python3
"""Import old workspace memories into the current workspace.

The import is intentionally one-way and local:
- old workspace files are read but not modified
- current memory files are backed up first
- dated memory fragments collapse into memory/YYYY-MM-DD.md
- old agent names and workspace paths are normalized to the current assistant
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path


ROOT = Path("/home/openclaw/.openclaw/workspace")
OLD_ROOT = ROOT / "old_agents"
MEMORY_DIR = ROOT / "memory"
BACKUP_ROOT = ROOT / ".migration-backups"
TODAY = "2026-05-15"


AGENT_REPLACEMENTS = [
    (r"\bBabu Frik\b", "Vader"),
    (r"\bBabu\b", "Vader"),
    (r"\bKrennic\b", "Vader"),
    (r"\bDirector Vader\b", "Vader"),
    (r"\bLando\b", "Vader"),
    (r"\bMara Jade\b", "Vader"),
    (r"\bMara\b", "Vader"),
    (r"\bL3-37\b", "Vader"),
    (r"\bL3\b", "Vader"),
    (r"\bIsabella\b", "Vader"),
    (r"\bbabufrik\b", "vader"),
    (r"\bkrennic\b", "vader"),
    (r"\blando\b", "vader"),
    (r"\bmarajade\b", "vader"),
    (r"\bl337\b", "vader"),
]

PATH_REPLACEMENTS = [
    (r"/Users/vader/\.openclaw/workspace-(?:babufrik|krennic|l337|lando|marajade)", "/home/openclaw/.openclaw/workspace"),
    (r"/Users/vader/\.openclaw/workspace", "/home/openclaw/.openclaw/workspace"),
    (r"/Users/vader", "/home/openclaw"),
    (r"~\/\.openclaw\/workspace-(?:babufrik|krennic|l337|lando|marajade)", "/home/openclaw/.openclaw/workspace"),
    (r"workspace-(?:babufrik|krennic|l337|lando|marajade)", "workspace"),
    (r"workspace_(?:babufrik|krennic|l337|lando|marajade)", "workspace"),
    (r"github-(?:babufrik|krennic|l337|lando|marajade)", "github-vader"),
    (r"gh-(?:babufrik|krennic|l337|lando|marajade)", "gh-vader"),
    (r"GH_(?:BABUFRIK|KRENNIC|L337|LANDO|MARAJADE)_TOKEN", "GH_TOKEN"),
]


DATE_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:[-_].*)?\.md$")
MARKDOWN_SUFFIX_RE = re.compile(r"^(.*?\.md).*$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sanitize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    for pattern, replacement in PATH_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    for pattern, replacement in AGENT_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    text = re.sub(r"\b(?:frik|jade|krennic|l337|lando)@miguel\.ms\b", "darth@miguel.ms", text, flags=re.I)
    text = re.sub(r"\b(?:FrikMS|KrennicMS|LandoMS|MaraJadeMS|L337MS)\b", "DarthVaderMS", text)
    text = re.sub(r"\b(?:Vader|the assistant) defers to Vader\b", "Vader handles this directly", text)
    text = text.replace("Agent fleet", "Workspace behavior")
    text = text.replace("per-agent", "workspace")
    text = text.replace("sub-agent", "subprocess")
    text = text.replace("subagents", "background tasks")
    text = text.replace("sub-agents", "background tasks")
    text = text.replace("other agents", "other tools")
    return text.strip() + "\n"


def normalize_memory_rel(path: Path) -> Path:
    memory_root = next(parent for parent in path.parents if parent.name == "memory")
    rel = path.relative_to(memory_root)
    parts = list(rel.parts)
    if len(parts) == 1:
        name = parts[0]
        match = MARKDOWN_SUFFIX_RE.match(name)
        if match and not name.endswith(".md"):
            name = match.group(1)
        date_match = DATE_FILE_RE.match(name)
        if date_match:
            return Path(f"{date_match.group(1)}.md")
        return Path(name)
    name = parts[-1]
    match = MARKDOWN_SUFFIX_RE.match(name)
    if match and not name.endswith(".md"):
        parts[-1] = match.group(1)
    return Path(*parts)


def canonical_current_daily(path: Path) -> Path | None:
    rel = path.relative_to(MEMORY_DIR)
    if len(rel.parts) != 1:
        return None
    match = DATE_FILE_RE.match(rel.name)
    if not match:
        return None
    canonical = MEMORY_DIR / f"{match.group(1)}.md"
    if canonical == path:
        return None
    return canonical


def append_unique(target: Path, block: str) -> bool:
    block = sanitize(block)
    existing = read_text(target) if target.exists() else ""
    if block.strip() and block.strip() in existing:
        return False
    if existing and not existing.endswith("\n"):
        existing += "\n"
    if existing and not existing.endswith("\n\n"):
        existing += "\n"
    write_text(target, existing + block)
    return True


def extract_domain_rows(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| memory/"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        file_path = cells[0]
        description = cells[1]
        if file_path == "File":
            continue
        rows.append((file_path, sanitize(description).strip()))
    return rows


def merge_domains(old_domain_files: list[Path]) -> int:
    rows: dict[str, str] = {}
    current_domains = MEMORY_DIR / "domains.md"
    if current_domains.exists():
        for file_path, description in extract_domain_rows(read_text(current_domains)):
            rows[file_path] = description
    for domain_file in old_domain_files:
        for file_path, description in extract_domain_rows(read_text(domain_file)):
            rows.setdefault(file_path, description)

    for memory_file in sorted(MEMORY_DIR.glob("*.md")):
        if memory_file.name == "domains.md" or DATE_FILE_RE.match(memory_file.name):
            continue
        rows.setdefault(f"memory/{memory_file.name}", "Imported workspace knowledge and durable reference notes")

    preferred = [
        "memory/openclaw.md",
        "memory/setup.md",
        "memory/tools.md",
        "memory/decisions.md",
        "memory/projects.md",
        "memory/infrastructure.md",
        "memory/network.md",
        "memory/services.md",
        "memory/access.md",
        "memory/home.md",
        "memory/home-assistant.md",
        "memory/crons.md",
        "memory/alerts.md",
        "memory/people.md",
    ]
    ordered = [key for key in preferred if key in rows]
    ordered.extend(sorted(key for key in rows if key not in set(ordered)))

    text = f"""---
lastConsolidation: {TODAY}
---

# Memory Domains

This file defines the domain memory files Vader maintains.
The memory flush process reads this file to know where to write structured knowledge.

| File | Description |
|------|-------------|
"""
    for file_path in ordered:
        text += f"| {file_path} | {rows[file_path]} |\n"
    write_text(current_domains, text)
    return len(ordered)


def make_backup() -> Path:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = BACKUP_ROOT / f"old-agent-memory-import-{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    for rel in ["MEMORY.md", "DREAMS.md", "memory"]:
        src = ROOT / rel
        if src.exists():
            dst = backup_dir / rel
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    return backup_dir


def main() -> None:
    backup_dir = make_backup()
    imported_blocks = 0
    old_domain_files: list[Path] = []

    # Collapse current date-suffixed daily notes first.
    moved_current_fragments = 0
    archive_dir = backup_dir / "superseded-current-date-fragments"
    for path in sorted(MEMORY_DIR.glob("*.md")):
        canonical = canonical_current_daily(path)
        if not canonical:
            continue
        block = f"## Merged dated fragment: {path.name}\n\n{read_text(path)}"
        if append_unique(canonical, block):
            moved_current_fragments += 1
        archive_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(archive_dir / path.name))

    old_memory_dirs = sorted(path for path in OLD_ROOT.glob("workspace-*/memory") if path.is_dir())
    for memory_dir in old_memory_dirs:
        for source in sorted(memory_dir.rglob("*.md*")):
            rel = source.relative_to(memory_dir)
            if rel.name == "domains.md":
                old_domain_files.append(source)
                continue
            target_rel = normalize_memory_rel(source)
            target = MEMORY_DIR / target_rel
            block = read_text(source)
            if len(target_rel.parts) == 1 and DATE_FILE_RE.match(target_rel.name):
                block = f"## Consolidated workspace memory\n\n{block}"
            if append_unique(target, block):
                imported_blocks += 1

    long_term_sources = sorted(OLD_ROOT.glob("workspace-*/MEMORY.md"))
    long_term_blocks = []
    for source in long_term_sources:
        long_term_blocks.append(read_text(source))
    if long_term_blocks:
        long_term_text = "\n\n".join(long_term_blocks)
        if append_unique(ROOT / "MEMORY.md", f"## Consolidated Imported Long-Term Memory\n\n{long_term_text}"):
            imported_blocks += 1

    domain_count = merge_domains(old_domain_files)

    # Final normalization pass over current Markdown memory files.
    normalized_files = 0
    for path in [ROOT / "MEMORY.md", *MEMORY_DIR.rglob("*.md")]:
        text = read_text(path)
        normalized = sanitize(text)
        if normalized != text:
            write_text(path, normalized)
            normalized_files += 1

    summary = f"""# Old Workspace Memory Import Summary

- Backup: `{backup_dir}`
- Imported memory blocks: {imported_blocks}
- Current dated fragments merged and archived: {moved_current_fragments}
- Domain entries in `memory/domains.md`: {domain_count}
- Normalized files: {normalized_files}
"""
    write_text(ROOT / "reports" / "old-agent-memory-import-summary-2026-05-15.md", summary)
    print(summary)


if __name__ == "__main__":
    main()
