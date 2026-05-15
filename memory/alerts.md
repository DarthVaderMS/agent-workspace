---
name: Active Alerts & Action Items
description: Critical issues, security alerts, deadlines, and action items requiring attention
type: project
---

# Active Alerts & Action Items

## 🔴 URGENT (Passed Deadlines)

### GitHub 2FA Enforcement — PAST DEADLINE
- **Accounts affected:** DarthVaderMS, DarthVaderMS
- **Original deadline:** April 18, 2026 (PASSED)
- **Status:** ⚠️ Action still needed — enable 2FA on both accounts
- **Impact:** GitHub will lock out accounts without 2FA
- **Evidence:** Multiple email alerts received 2026-04-12 through 2026-04-20
- **How to apply:** Log in to each GitHub account and enable 2FA via Settings > Security

### GitHub Account Security Activity (2026-04-15)
- **What happened:** Password reset + passkey added to GitHub account
- **Emails:** 8 notifications total (password, passkey, 4x recovery codes reminders)
- **Status:** Need to verify if this was intentional
- **Action:** Review GitHub account login history to confirm no unauthorized access

---

## 🟡 HIGH PRIORITY (Action Needed)

### OpenClaw Daily Backup NFS Copy Failure
- **Issue:** Backup archive creation passed, but rsync copy to `/home/openclaw/nfs/nas-backups/systems/openclaw/` failed with `Operation not permitted`
- **Observed:** 2026-05-13 daily backup run
- **Impact:** Local backup may exist, but NAS/NFS copy did not complete
- **Fix needed:** Check NFS mount permissions/export/user mapping for the Linux `openclaw` host

### WhatsApp Sync Broken — wacli Outdated
- **Issue:** wacli client version mismatch (HTTP 405 Client Outdated error)
- **Impact:** WhatsApp message sync disabled since ~2026-03-15
- **Local DB:** Stale — last message on record: March 15, 2026
- **Fix:** Run `brew upgrade steipete/tap/wacli` or `go install github.com/steipete/wacli@latest`
- **Frequency:** Daily WhatsApp report affected; Discord #comms gets "quiet day" msgs

### GA4 Permission Error — SEO Daily Report
- **Issue:** Service account lacks permissions for GA4 property 377775150
- **Error:** `HttpError 403 — User does not have sufficient permissions`
- **Impact:** Daily SEO Report cron job fails (23+ consecutive errors as of 2026-04-18)
- **Status:** Recurring daily; script never completes
- **Fix needed:** Grant service account read access to GA4 property or use a different auth method

### SEO Sitemap Sync Timeout — SIGTERM Kills Script
- **Issue:** Script killed mid-run before processing all 35+ URLs
- **Impact:** GSC inspection incomplete daily; only ~17-20 URLs inspected instead of all
- **Root cause:** GSC API rate-limited to 1 req/sec; 35+ URLs takes 35-40s but cron times out sooner
- **Workaround:** Run manually with longer timeout: `timeout 120 python3 scripts/seo-sitemap-gsc-sync.py`
- **Fix needed:** Extend cron timeout or paginate inspection across multiple runs

### Slack Configuration Stale
- **Issue:** OpenClaw Docs weekly sync cron targets Slack session key, but Slack not configured in openclaw.json
- **Impact:** Docs sync fails to deliver to Slack; Discord gets it instead (fallback)
- **Status:** As of 2026-04-18, only Discord + WhatsApp are configured
- **Fix:** Update `f3a62e6f-c235-4aad-a7a6-0ec9b401ff7a` cron delivery to target Discord #openclaw-settings

### Workspace GitHub Sync SIGTERM (2026-05-01)
- **Issue:** Daily workspace sync exited with SIGTERM after reporting `workspace: committed`
- **Impact:** Sync status uncertain/incomplete; at least one workspace commit happened before termination
- **Action needed:** Re-run or inspect `sync-workspaces-to-github.sh` execution path to find timeout/termination cause and confirm pending pushes

---

## 🟢 MONITORING (Lower Priority)

### Email Tooling Guardrail — gog only
- **Rule:** Use `gog` only for email checks. Never use Codex Gmail connector/tools or MCP Gmail tools, even read-only.
- **Reason:** The Gmail connector can be account-ambiguous and previously returned `joao@miguel.ms` when the safe default intent was `darth@miguel.ms`.
- **If blocked:** Report that `gog` is unavailable/unauthenticated/cannot select account; do not fall back.

### QMD memory backend — repaired 2026-05-13
- **Issue fixed:** `better-sqlite3` in the Bun-global QMD install had been compiled for Node module ABI 127 while Node v24.15.0 requires ABI 137
- **Action taken:** Ran `npm rebuild better-sqlite3` in `/home/openclaw/.bun/install/global/node_modules/@tobilu/qmd`, refreshed Vader's QMD index, and regenerated missing embeddings
- **Verification:** `qmd status`, `qmd search`, and `qmd vsearch` pass under this OpenClaw QMD environment

### Google AI Studio Usage Tier Review
- **Status:** Reminder sent; action needed before end of April 2026
- **What to do:** Log in to Google AI Studio and review usage tier to avoid service disruption

### Confluence Docs Sync Issues (2026-04-18)
- **Status:** Completed successfully; created local report
- **Known blockers:** Slack bot token unavailable, Confluence API update attempts skipped
- **Resolution:** Manual report created → `memory/confluence-sync-report-2026-04-18.md`

### Session Cleanup Command Failures
- **Issue:** `openclaw sessions cleanup` commands abort/fail with no output
- **Frequency:** Daily cron runs encounter this; hard to diagnose
- **Workaround:** Session store maintenance completed manually on 2026-04-13 (29 Claude, 7 Codex entries retained)
- **Impact:** Low — cleanup still happens via fallback methods

---

**Last Updated:** 2026-04-21

**Why:** Consolidates active issues and deadlines in one place to prevent missed action items and recurring failures.

**How to Apply:** 
1. Check this list daily for any URGENT items that crossed their deadline
2. 🔴 URGENT requires immediate action
3. 🟡 HIGH PRIORITY should be fixed this week
4. 🟢 MONITORING can be addressed in the next sprint
