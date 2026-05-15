---
name: SEO Sync Status
description: SEO/GSC/GA4 access status, gog-based reporting path, and legacy sitemap sync context
type: project
---

# SEO, Google Search Console, and GA4 Access

## Current Status (as of 2026-05-15)

- **Primary access path:** `gog` with account `darth@miguel.ms`
- **Known working command environment:** `HOME=/home/openclaw gog ... --account darth@miguel.ms`
- **Google Cloud project for API enablement:** `openclaw-486417`
- **Enabled APIs:** `analyticsdata.googleapis.com`, `analyticsadmin.googleapis.com`, `searchconsole.googleapis.com`
- **GA4 access:** `gog analytics accounts --account darth@miguel.ms` works and returns account `269244269` (`miguel.ms`) with 1 property.
- **Search Console access:** `gog searchconsole sites list --account darth@miguel.ms` works and returns both `https://miguel.ms/` and `sc-domain:miguel.ms` with `siteFullUser`.
- **Preferred GSC property for URL-specific work:** `https://miguel.ms/`
- **Domain-wide GSC property:** `sc-domain:miguel.ms`

Use `gog` directly for SEO/GSC/GA4 reads instead of relying on the old internal Python scripts when possible.

## Useful Commands

```bash
HOME=/home/openclaw gog analytics accounts --account darth@miguel.ms
HOME=/home/openclaw gog searchconsole sites list --account darth@miguel.ms
HOME=/home/openclaw gog searchconsole sites get 'https://miguel.ms/' --account darth@miguel.ms
HOME=/home/openclaw gog searchconsole query 'https://miguel.ms/' --account darth@miguel.ms --from YYYY-MM-DD --to YYYY-MM-DD --dimensions query --max 100
HOME=/home/openclaw gog searchconsole query 'sc-domain:miguel.ms' --account darth@miguel.ms --from YYYY-MM-DD --to YYYY-MM-DD --dimensions query --max 100
```

## Legacy Internal Script Context

The older SEO sync path used `python3 scripts/seo-sitemap-gsc-sync.py` and `scripts/seo-daily-report.py`. Keep these notes as historical context, but prefer `gog` for current GA4/Search Console access.

- **Last known sitemap status (2026-05-13):** 40 sitemap URLs, 13 indexed in GSC, 27 inside the 7-day cooldown window.
- **Old daily script:** `python3 scripts/seo-sitemap-gsc-sync.py` (formerly 9AM Europe/Lisbon)
- **2026-05-15 migration:** Miguel provided the old script for cron import, but it still used `/Users/vader`, `/opt/homebrew`, a missing service-account key, and missing Python Google dependencies on this Linux host. It was adapted into `scripts/seo-sitemap-gsc-sync.py` using `gog` for Search Console reads.
- **Current cron:** `SEO Sitemap ↔ GSC Daily Sync` (`0d30d420-3561-477d-8170-230c27bb57fe`) runs daily at 09:00 Europe/Lisbon and delivers to Discord `#miguel-ms-seo` (`1487123302211391578`).
- **Current weekly content cron:** `Weekly Content Analysis Report` (`32491bd8-3297-46fd-b933-d92a32c2a2ed`) runs Mondays at 06:00 Europe/Lisbon and delivers to Discord `#miguel-ms-seo` (`1487123302211391578`).
- **Current visibility method:** Search Console Search Analytics page rows from the last 90 days are used as a visibility/indexing proxy. This is not the same as URL Inspection API coverage.
- **Current script contract:** `python3 scripts/seo-sitemap-gsc-sync.py` logs to stderr, writes `memory/seo-sync-latest-report.txt` and `memory/seo-sync-state.json`, and emits the Discord payload to stdout wrapped in `<output>...</output>`.
- **Current weekly content script contract:** `python3 scripts/weekly-content-analysis-report.py` logs to stderr, writes `memory/seo-weekly/<ISO-week>.json` and `memory/seo-weekly-latest-report.txt`, and emits the Discord payload to stdout wrapped in `<output>...</output>`.

## Known Issues

### 1. Legacy Script Timeout/SIGTERM Kills Mid-Run
- **Symptom:** Script gets terminated by SIGTERM before processing all URLs
- **Impact:** GSC inspection API only runs against ~17-20 URLs per run, missing 15+ URLs daily
- **Root Cause:** GSC URL Inspection API rate-limited to ~1 req/sec; 35+ URLs = 35-40s execution, cron timeout shorter
- **Current direction:** Prefer `gog` for Search Console and GA4 reads. If the legacy URL Inspection script remains needed, paginate inspection across multiple cron runs or increase timeout.

### 2. Python 3.9 Compatibility (FIXED 2026-04-20)
- **Issue:** PEP 604 union types (`Type | None`) not supported in Python 3.9
- **Status:** ✅ Fixed — changed to `typing.Optional[Type]`
- **Date fixed:** 2026-04-20

### 3. SSL Transient Error (2026-04-20)
- **Error:** `BLOCK_CIPHER_PAD_IS_WRONG` during GSC API call
- **Type:** Transient (SSL/TLS padding issue, likely API hiccup)
- **Status:** Not blocking; next auto-retry likely succeeds
- **Frequency:** Rare

## API Details

- **GSC URL Inspection API Rate Limit:** ~1 request per second
- **Current access:** `gog` OAuth as `darth@miguel.ms`
- **Cooldown Strategy:** 7-day cooldown before re-pushing same URL (implemented as of 2026-04-08)
  - Prevents repeated hammering of URLs Google hasn't crawled yet
  - Respects Google's recommendation: push only on content new/update

## Report Output

- **Location:** `memory/seo-sync-latest-report.txt`
- **Posted to:** Discord #miguel-ms-seo channel
- **Refresh:** Daily after script completes (or on retry)

## Recent Reports

- **2026-05-13:** 40 URLs, 13 indexed / 27 inside 7-day cooldown; script completed successfully
- **2026-04-20:** 38 URLs, 14 indexed / 24 not indexed (script completed successfully after Python fix)
- **2026-04-19:** Timeout (stale report from 2026-04-18 used)
- **2026-04-18:** Timeout (report stale from 2026-04-17)
- **2026-04-13:** 35 URLs, 14 indexed / 21 not indexed

---

**Why:** SEO visibility and indexing checks are important for Miguel's site. Current reads should use `gog` against GA4/Search Console, with the old scripts treated as legacy automation until replaced or retired.

**How to Apply:** When seeing stale SEO reports or timeout errors, consider:
1. Manually run the script with `timeout 120 python3 scripts/seo-sitemap-gsc-sync.py`
2. Or split the sitemap inspection across 2 sequential cron jobs (first 20 URLs, then 20+ URLs)
3. Check Python version compatibility if script fails immediately
