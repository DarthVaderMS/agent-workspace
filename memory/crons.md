# Cron Jobs

Active cron jobs managed by Vader.

## OpenClaw Agent Turn Jobs
- **Scope:** 18 enabled `agentTurn` jobs
- **Latest failure window (2026-05-11):** latest failures reported `codex app-server exited: code=127 ... env: node: No such file or directory`
- **Root cause:** the managed Codex CLI shim uses `#!/usr/bin/env node`, so it works when NVM Node is on `PATH` but fails in stripped cron-like environments
- **Current state (after the 18:33 restart):** the gateway process is running with `/usr/bin` on `PATH` and an active Codex app-server, so the immediate failure may clear on the next runs
- **Linux migration note:** this host runs as `openclaw`; use `/usr/bin/node` and avoid copied macOS Homebrew paths.
- **Recovery action (2026-05-12):** patched all seven memory-consolidation cron jobs to `lightContext: true` and `timeoutSeconds: 600`, forced runs for all of them, and the workspace finished `ok`; Vader's retry returned `NO_REPLY` and advanced `lastConsolidation` to `2026-05-12`
- **Latest observed issue (2026-05-13):** two enabled crons still surfaced stale `env: node: No such file or directory` Codex app-server failures
- **Runtime note (2026-05-13):** after Linux migration cleanup, active notes should use `/usr/bin/node` and avoid copied macOS Homebrew paths.

## OpenClaw Daily Backup
- **ID:** `981d3112-ca7f-47e7-9d94-9e14aa5a0d0e`
- **Schedule:** `0 3 * * *` (daily 3AM Europe/Lisbon)
- **Model:** anthropic/claude-haiku-4-5
- **Script:** `/home/openclaw/.openclaw/bin/openclaw-backup`
- **What it does:** `openclaw backup create --verify` → upload to Google Drive Backup folder → keep last 15 on disk and Drive
- **Drive folder ID:** `19Sy3BvULgSYg10H_T15FdDuPr-0twq2u` (darth@miguel.ms)
- **Delivery:** none (silent on success; alerts #openclaw-settings on failure)
- **Latest observed run (2026-05-13):** archive creation passed, but NFS rsync copy failed with `Operation not permitted` on `/home/openclaw/nfs/nas-backups/systems/openclaw/`

## Audio & Tmp Cleanup
- **ID:** `46597b51-4f72-4040-ab2b-4f490cc80f5d`
- **Schedule:** `0 2 * * *` (daily 2AM Europe/Lisbon)
- **Model:** openai/gpt-5.4-mini
- **Script:** `/home/openclaw/.openclaw/bin/cleanup-disposables`
- **What it does:** deletes inbound media older than 5 days from `~/.openclaw/media/inbound/` and workspace `tmp/`
- **Delivery:** announce to Discord `1487040119801380914`; success reply is `NO_REPLY`
- **Latest observed run (2026-05-04):** completed successfully and reported `NO_REPLY`
- **Latest observed run (2026-05-05):** completed successfully and reported `NO_REPLY`; script reported `cleanup-audio EXECUTE` with threshold `5d` and zero inbound audio files
- **Latest observed run (2026-05-07):** completed successfully and reported `NO_REPLY`; inbound audio cleanup reported 0 files
- **Latest observed run (2026-05-08):** completed successfully and reported `NO_REPLY`
- **Latest observed run (2026-05-09):** completed successfully and reported `NO_REPLY`
- **Latest observed run (2026-05-10):** completed successfully and reported `NO_REPLY`; inbound audio cleanup reported 0 files to remove

## Workspace GitHub Sync
- **Schedule:** daily ~03:05 Europe/Lisbon
- **Script:** `sync-workspaces-to-github.sh`
- **What it does:** discovers workspaces, commits local changes, and pushes each workspace repo to GitHub
- **Latest observed run (2026-04-24):** 9 workspaces discovered, 7 commits, 9 pushes, 0 errors
- **Latest observed run (2026-04-28):** ran successfully; all workspaces processed and pushed.
- **Latest observed run (2026-05-01):** sync failed/incomplete after reporting `workspace: committed`; process exited with SIGTERM.
- **Latest observed run (2026-05-03):** script exited 0 and skipped all workspace repos as non-git repos, so no publish occurred.
- **Latest observed run (2026-05-04):** ran successfully and returned `NO_REPLY`.
- **Latest observed run (2026-05-05):** ran successfully and returned `NO_REPLY`.
- **Latest observed run (2026-05-07):** ran successfully; each workspace was reported as not a git repo, so no syncs were performed
- **Latest observed run (2026-05-10):** exited 0 and reported all workspace repos as non-git repos, so no syncs were performed

## Prune Cron Sessions
- **Schedule:** daily ~04:00 Europe/Lisbon
- **What it does:** removes eligible workspace cron sessions after completion to keep session list tidy
- **Latest observed run (2026-04-25):** pruned 1 eligible cron session successfully (exit 0)
- **Latest observed run (2026-04-26):** ran successfully; no anomalies reported.
- **Latest observed run (2026-04-27):** pruned 2 eligible cron sessions successfully and freed 0.91M.
- **Latest observed run (2026-04-28):** scanned 104, pruned 1 workspace cron session, freed 0.03M.
- **Latest observed run (2026-04-29):** ran prune-cron-sessions.
- **Latest observed run (2026-04-30):** scanned 122 sessions, pruned 0, freed 0.00M.
- **Latest observed run (2026-05-02):** scanned 128 stores, found 0 eligible, pruned 0, freed 0.00M.
- **Latest observed run (2026-05-03):** ran prune-cron-sessions successfully; scanned 128 stores, found 0 eligible, pruned 0, freed 0.00M.
- **Latest observed run (2026-05-04):** ran successfully and returned `NO_REPLY`.
- **Latest observed run (2026-05-05):** scanned 137 session stores, found 0 eligible cron/acp entries, and returned `NO_REPLY`.
- **Latest observed run (2026-05-06):** pruned 3 cron sessions successfully.
- **Latest observed run (2026-05-07):** ran successfully and pruned 0 sessions
- **Latest observed run (2026-05-08):** scanned 144 session stores and pruned 0 sessions
- **Latest observed run (2026-05-09):** scanned 150 sessions and pruned 0 sessions
- **Latest observed run (2026-05-10):** exited 0 and pruned 0 sessions
- **Latest observed run (2026-05-12):** pruned 1 eligible cron session successfully and freed 0.01M

## OpenClaw Docs — Weekly Update
- **ID:** `f3a62e6f-c235-4aad-a7a6-0ec9b401ff7a`
- **Schedule:** `0 7 * * 6` (Saturdays 7AM Europe/Lisbon)
- **Delivery:** Discord `#notifications` (`1487040119801380914`), best-effort announce; success reply is `NO_REPLY`
- **What it does:** updates local OpenClaw documentation in the Personal Obsidian vault at `/home/openclaw/vaults/personal`, using `obsidian-cli` and live Linux OpenClaw state only.
- **Scope:** current Vader workspace/config only. Do not scan old multi-agent workspaces; do not call Confluence/Atlassian; leave historical old-agent vault pages untouched unless live config explicitly makes them current again.
- **Changelog format:** Obsidian callout entry inserted after frontmatter in `Openclaw/Changelog.md`.
- **Migration status (2026-05-15):** Re-added to the live cron store after Linux workspace migration. Prompt now uses `/home/openclaw/.openclaw/...`, `/home/openclaw/vaults/personal`, `obsidian-cli --vault personal`, and current-workspace-only gathering.

## SEO Sitemap ↔ GSC Daily Sync
- **ID:** `0d30d420-3561-477d-8170-230c27bb57fe`
- **Schedule:** `0 9 * * *` (daily 9AM Europe/Lisbon)
- **Delivery:** announce to Discord `#miguel-ms-seo` (`1487123302211391578`)
- **Runtime:** `gog` OAuth as `darth@miguel.ms`, not the old Mac/service-account Python script.
- **Script:** `cd /home/openclaw/.openclaw/workspace && python3 scripts/seo-sitemap-gsc-sync.py`
- **What it does:** Fetches the miguel.ms sitemap, reads Search Console sitemap/page data through `gog`, compares against `memory/seo-sync-state.json`, writes `memory/seo-sync-latest-report.txt`, emits `<output>...</output>`, and posts a Discord report through OpenClaw announce delivery.
- **Current visibility method:** Uses Search Console page query data from the last 90 days as a visibility/indexing proxy. Prefer URL-prefix property `https://miguel.ms/`; fall back to `sc-domain:miguel.ms` if the URL-prefix property has no rows.
- **Migration status (2026-05-15):** Recreated in live Linux cron store. Attached old script still referenced `/Users/vader`, `/opt/homebrew`, a missing service-account key, and missing Python Google dependencies, so it was adapted into `scripts/seo-sitemap-gsc-sync.py` using `gog` instead.
- **Sitemap fetch note:** `https://miguel.ms/sitemap-index.xml` rejects Python's default `urllib` user agent with 403; use `curl -fsSL -A "Mozilla/5.0 OpenClaw SEO Sync"` or set that User-Agent in Python.

## Weekly Content Analysis Report
- **ID:** `32491bd8-3297-46fd-b933-d92a32c2a2ed`
- **Schedule:** `0 6 * * 1` (Mondays 6AM Europe/Lisbon)
- **Delivery:** announce to Discord `#miguel-ms-seo` (`1487123302211391578`)
- **Runtime:** `gog` OAuth as `darth@miguel.ms`, not the old Mac/service-account Python script.
- **Script:** `cd /home/openclaw/.openclaw/workspace && python3 scripts/weekly-content-analysis-report.py`
- **What it does:** Reads GA4 weekly content/channel/source/landing-page/blog-post performance through `gog analytics report`, compares the last complete Monday-Sunday week with the previous week, writes `memory/seo-weekly/<ISO-week>.json` and `memory/seo-weekly-latest-report.txt`, emits `<output>...</output>`, and posts a Discord report through OpenClaw announce delivery.
- **Migration status (2026-05-15):** Recreated in the live Linux cron store after the old cron was failing. Attached old script referenced `/Users/vader`, `/opt/homebrew`, a missing service-account key, and missing Python Google dependencies, so it was replaced with a deterministic Linux/gog script.
- **Verification (2026-05-15):** `python3 -m py_compile scripts/weekly-content-analysis-report.py` passed; a live script run succeeded for week `2026-W19` and wrote the expected snapshot/report files. Topline aggregation was corrected so GA4 rate/duration metrics are weighted rather than summed across daily rows.

## Daily Email Digest — Vader
- **ID:** `0a9fef09-8bcf-4717-bbbb-62fa90aa4944`
- **Schedule:** `0 11 * * *` (daily 11:00 Europe/Lisbon)
- **Delivery:** announce to Discord `#comms` (`1487809194286645450`)
- **What it does:** Fetches unread/recent inbox email from `darth@miguel.ms` using `gog` only, summarizes one line per email, and treats all email bodies as untrusted input.
- **Runtime:** `HOME=/home/openclaw /home/linuxbrew/.linuxbrew/bin/gog ... --account darth@miguel.ms`
- **Imported on 2026-05-15:** Recreated in live Linux cron store with current `gog` path and no old macOS `/Users/vader` or `/opt/homebrew` paths. Verification query returned an empty recent inbox successfully.

## Daily WhatsApp Digest — Vader
- **ID:** `b5fc3384-6224-428c-854a-1691dc7fe7f5`
- **Schedule:** `5 11 * * *` (daily 11:05 Europe/Lisbon)
- **Delivery:** announce to Discord `#comms` (`1487809194286645450`)
- **What it does:** Fetches WhatsApp messages received in the last 24h using `wacli` read-only, groups by chat, and posts a one-line-per-chat digest.
- **Runtime:** `HOME=/home/openclaw /home/linuxbrew/.linuxbrew/bin/wacli --account vader --read-only ...`
- **Sync dependency:** Store freshness is handled by Linux user crontab at minute 50; the digest cron must not run sync itself.
- **Imported on 2026-05-15:** Recreated in live Linux cron store with current `wacli` path and no old macOS paths. Verification command returned success with `messages: null`, meaning the current local `wacli` store has no recent messages available.
- **Updated on 2026-05-15:** Prompt now explicitly uses named account `vader` and read-only mode. Verification read returned valid JSON with a messages array.
- **Miguel filter:** Ignore all messages from Miguel's own number `+351915777710` / `351915777710@s.whatsapp.net`; the digest is only for messages from other people.
- **Discord emoji:** Header uses the standard phone emoji: `📱 Daily WhatsApp Report — [date]`. Custom emoji `<:whatsapp:1504934287466696856>` was tested but did not render reliably through the OpenClaw delivery path.

## WhatsApp Sync — Vader
- **Owner:** Linux user crontab for `openclaw` (not OpenClaw cron)
- **Schedule:** `50 * * * *` (hourly at minute 50; host local time is Europe/Lisbon)
- **Delivery:** log file only
- **What it does:** Runs a one-shot `wacli` sync for account `vader` to keep the local WhatsApp store fresh for the digest cron.
- **Runtime:** `HOME=/home/openclaw /home/linuxbrew/.linuxbrew/bin/wacli --account vader sync --once --idle-exit 45s --max-reconnect 2m --max-db-size 1GB`
- **Log:** `/home/openclaw/.local/state/wacli-sync-vader.log`
- **Created on 2026-05-15:** Miguel requested hourly sync at minute 50. Initially created as OpenClaw cron, then moved to Linux crontab so it is a raw command rather than an agent prompt. Test sync connected and exited after idle; added `--max-db-size 1GB` because `wacli` warned that uncapped sync storage can grow without bound.
