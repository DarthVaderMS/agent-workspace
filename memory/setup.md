# Setup & Integrations

Seed notes for tooling setup, environment notes, and integrations.

## 2026-05-13 — Codex isolated HOME note

- The `openclaw` CLI inside Codex isolated HOME still resolves `~/.openclaw/openclaw.json` to the wrong home unless `OPENCLAW_STATE_DIR=/home/openclaw/.openclaw` is set

## Cron Runtime

- This host is Linux, running as Unix user `openclaw` with home `/home/openclaw`; do not use copied macOS home paths.
- `node` is available at `/usr/bin/node`; cron-like commands should not assume macOS Homebrew paths.
- `gog` is available at `/home/linuxbrew/.linuxbrew/bin/gog`; its config/token files are under `/home/openclaw/.config/gogcli`.

## Default Time Zone

- Default to `Europe/Lisbon` for reminders, scheduling, timestamps, and date interpretation unless Miguel explicitly specifies another timezone.
- Use the IANA timezone name instead of fixed UTC offsets because Lisbon changes with DST.

## Email Tooling Policy

- Email checks must use `gog` only.
- Never use Codex Gmail connectors, MCP Gmail tools, or other Codex-provided email tools to read/check email, even read-only.
- If `gog` is unavailable, unauthenticated, or cannot select the required account, stop and report the blocker instead of falling back.
- Known working Vader email command environment: `HOME=/home/openclaw XDG_CONFIG_HOME=/home/openclaw/.config gog ... --account darth@miguel.ms`.

## Google SEO Tooling

- `gog` is also the current preferred access path for Google Analytics and Google Search Console.
- Use `HOME=/home/openclaw gog ... --account darth@miguel.ms` so the command sees the real `/home/openclaw/.config/gogcli` OAuth config instead of the agent sandbox home.
- `darth@miguel.ms` has `gog` OAuth services: `analytics,calendar,contacts,docs,drive,gmail,searchconsole,sheets`.
- Enabled GCP APIs in project `openclaw-486417`: `analyticsdata.googleapis.com`, `analyticsadmin.googleapis.com`, and `searchconsole.googleapis.com`.
- Verified GA4 access: account `269244269` (`miguel.ms`) is visible through `gog analytics accounts`.
- Verified Search Console access: both `https://miguel.ms/` and `sc-domain:miguel.ms` are visible with `siteFullUser`.
- Prefer `gog` over old internal SEO Python scripts for GA4/Search Console reads unless a task specifically needs legacy sitemap/indexing automation.

## WhatsApp History Tooling

- `wacli` is available at `/home/linuxbrew/.linuxbrew/bin/wacli`.
- Use `HOME=/home/openclaw /home/linuxbrew/.linuxbrew/bin/wacli --read-only ...` for cron-style WhatsApp history reads so it uses the real Linux home rather than the agent sandbox home.
- Current local store path with `HOME=/home/openclaw`: `/home/openclaw/.local/state/wacli`.
- As of 2026-05-15, `wacli doctor` reports no configured accounts/auth and the read-only messages query returns success with no messages; cron imports can run, but useful digests require a populated/authenticated `wacli` store.
- After linking on 2026-05-15, named account `vader` is authenticated as `351910299310@s.whatsapp.net`; use `--account vader`.
- For recurring sync, prefer the Linux user crontab entry over OpenClaw cron so the sync is a raw command, not an agent prompt. Current crontab runs hourly at minute 50 and logs to `/home/openclaw/.local/state/wacli-sync-vader.log`.

## SSH Client Setup

- SSH files live under `/home/openclaw/.ssh`.
- Standard modes: `.ssh` `700`, private keys/config/known_hosts/authorized_keys `600`, public keys `644`.
- Primary copied private key: `/home/openclaw/.ssh/id_ed25519_vader`.
- Keep `/home/openclaw/.ssh/config` updated as host access is verified. Miguel explicitly approved ongoing maintenance of host/user/key mappings.
- Default infrastructure SSH user is usually `root`; if root is not allowed, Miguel will say so or the verified config entry should record the exception.
