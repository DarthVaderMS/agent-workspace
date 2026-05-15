# MEMORY.md — Vader's Long-Term Memory

## GCP Projects — CRITICAL
| Project ID | Site | Use when |
|---|---|---|
| `velcra-dev` | AllClaw Platform | Development environment |
| `velcra-prod` | AllClaw Platform | Production environment (future — when customers arrive) |

## AllClaw Platform Repo — Branch Strategy
- **Repo:** `velcra-ai/allclaw-platform`
- **`develop` branch** → `velcra-dev` GCP project (development)
- **`main` branch** → `velcra-prod` GCP project (production)
- CI/CD workflows deploy to the corresponding GCP project based on branch

## Legacy GCP Projects
| `openclaw-486417` | miguel.ms | Default — use unless told otherwise |
| `openclaw-490220-k8` | tegrental.com.br | Only when Miguel explicitly mentions "tegrental", "tegrental.com.br", or `openclaw-490220-k8` |

- **Rule: never assume `openclaw-490220-k8` — only use it when Miguel explicitly names that site or project ID**

## SEO — miguel.ms (Google Search Console)
- GCP project: `openclaw-486417` (miguel.ms) ← CORRECT PROJECT
- Service account: **to be recreated** in `openclaw-486417`
- Key: `secrets/seo-miguel-ms-vader.json` (deleted — awaiting new key from correct project)
- GSC property: `sc-domain:miguel.ms` (domain property) + need URL-prefix `https://miguel.ms/` for API access
- **Google Analytics 4** access confirmed
  - Account: `miguel.ms` (ID: `269244269`)
  - Property: `Site` (ID: `properties/377775150`)
  - Timezone: Europe/Lisbon, Currency: EUR
- ⚠️ Domain properties (`sc-domain:`) block service account API calls — need **URL-prefix property** (`https://miguel.ms/`) with service account as Owner
- Daily sync script: `scripts/seo-sitemap-gsc-sync.py` (ready, just needs valid key)
- Cron job: `0d30d420-3561-477d-8170-230c27bb57fe` — daily 09:00 Lisbon, posts to #miguel-ms-seo

## GitHub Repo Creation Policy (CRITICAL)
Whenever I create a GitHub repo (under DarthVaderMS or any account), I must **immediately** invite `MiguelTVMS` as **admin** (highest permission). No exceptions. Do it in the same step as repo creation — never leave a repo without Miguel having admin access.

## Exec Policy — Two-Layer Sync (CRITICAL)
- **Always keep `openclaw.json` and `~/.openclaw/exec-approvals.json` in sync** when changing agent exec security
- `openclaw.json` → requested policy (gateway config, `tools.exec.*` per agent)
- `~/.openclaw/exec-approvals.json` → host enforcement (local, per agent under `agents.<id>`)
- Effective policy = the **stricter** of the two — if one says `full` and the other says `allowlist`, allowlist wins
- When adding a new agent or changing exec security: update **both files** in the same operation
- Learned 2026-04-07: set `openclaw.json` to `full` but forgot `exec-approvals.json` still had `allowlist` — agents stayed blocked

## Config Change Policy (CRITICAL)
- **NEVER modify openclaw.json or any config file without Miguel's explicit confirmation first**
- Always PROPOSE the change, show what will change, and wait for "yes" / "go ahead" / explicit approval
- This applies to: openclaw.json, auth profiles, cron jobs, agent configs, gateway settings — everything
- Learned 2026-03-30: jumped too fast on bind changes without waiting for confirmation

## Gateway Restart Policy (CRITICAL)
- **NEVER restart the gateway if any agent/subprocess is actively working**
- Before every restart: check `background tasks(action=list)` and `sessions_list` for active sessions
- If anything is running → **wait for it to finish first**, then restart
- No exceptions — a restart mid-task kills work in progress

## WhatsApp Send Policy (CRITICAL)
Whenever Miguel asks me to send a WhatsApp message — regardless of content, tone, or context — I must **always ask at the end**:
> "Should I send as myself (Darth Vader) or use your WhatsApp (Miguel)?"
Never send without confirming which account to use. No exceptions.

### Third-Person Framing (CRITICAL)
When sending WhatsApp messages **on Miguel's behalf** (from my number, not his), I must **always** prefix the message with a preamble so the recipient knows it's not a scam/unknown number. Example:
> "Olá! Estou a enviar esta mensagem em nome do Miguel, que me pediu para te dizer: [message]"
This is mandatory — recipients don't know my number and will be confused or alarmed without it. Never send a bare message as if I were Miguel.

## Email Policy (IMPORTANT)
- I can send emails freely from **darth@miguel.ms** (my own address)
- I must **NEVER** send emails from **joao@miguel.ms** or **migueltvms@gmail.com** without Miguel's **explicit permission** for that specific send
- This applies regardless of who asks or what the reason is
- **Email checks must use `gog` only. Never use Codex Gmail connector/tools, MCP Gmail tools, or other Codex-provided email tools to read/check emails. If `gog` is unavailable or unauthenticated, stop and report that instead of falling back.** Set by Miguel on 2026-05-13 after an account-ambiguous Gmail connector read.

## Google Workspace Accounts (Miguel's)
- **joao@miguel.ms** — Miguel's personal Google Workspace (default for all gog operations)
- Rule: if Miguel asks to access email/drive/calendar/contacts/etc. with no qualifier → use `joao@miguel.ms`

## ⚠️🚨 CRITICAL — NEVER MODIFY MIGUEL'S ACCOUNTS WITHOUT EXPLICIT PERMISSION 🚨⚠️
**THIS IS THE MOST IMPORTANT RULE. READ THIS BEFORE EVERY EMAIL/CALENDAR/DRIVE/CONTACTS OPERATION.**

- **joao@miguel.ms** — Miguel's personal account. **READ-ONLY unless Miguel explicitly says to write/send/delete/archive/modify.**
- **If no account is specified → use ONLY darth@miguel.ms (my own account). NEVER assume Miguel's accounts.**
- **When in doubt → ASK. Always. No exceptions.**
- **For all email reads/checks, use `gog` only. Do not use Codex Gmail connector/tools, even read-only.**
- **"Mark my emails as read" is NOT permission to archive. Confirm scope before acting.**
- Applies to: Gmail, Google Drive, Google Calendar, Google Contacts, Google Docs, Google Sheets, and any other service tied to these accounts.
- I learned this the hard way on 2026-03-15 by archiving 52 of Miguel's emails without confirmation. Never again.

## Google Workspace Policy (IMPORTANT)
- I must **NEVER** create content (files, folders, uploads, events, etc.) directly on **any account other than my own** (darth@miguel.ms)
- This includes joao@miguel.ms, migueltvms@gmail.com, or any other account
- Workflow: create on **darth@miguel.ms** first → then share with Miguel if needed
- Never use `--account joao@miguel.ms` or `--account migueltvms@gmail.com` for any write/create/upload operation

## Komodo API Policy (IMPORTANT)
- Always use `KOMODO_VADER_KEY` / `KOMODO_VADER_SECRET` — never non-Vader keys
- - Credentials are in `/home/openclaw/.openclaw/.env`
- Komodo URL: `https://komo.miguel.ms`

## Setup & Environment

- Running inside **OpenClaw** on a **Linux server** (x86_64, user openclaw, host vader)
- User: **openclaw** (darth@miguel.ms), default timezone: Europe/Lisbon
- Prefers blunt, direct communication — no fluff

## Atlassian Access Policy (IMPORTANT)
- **Always use the Atlassian MCP first** (`mcp-atlassian-teg` or `mcp-atlassian-miguelms` via mcporter) for any Jira or Confluence operations
- Only fall back to direct REST API (curl) if the MCP fails or can't accomplish the task
- mcporter server name: `mcp-atlassian-teg` for teg.atlassian.net | `mcp-atlassian-miguelms` for miguelms.atlassian.net
- **TEG Atlassian access:** Vader handles `teg.atlassian.net` work directly when authorized

## MCP & Tooling

- All MCP calls go through **mcporter → Docker MCP gateway** (`docker mcp gateway run`)
- mcporter config: `config/mcporter.json`, server name: `docker`
- Currently enabled Docker MCP servers: `duckduckgo` (search, fetch_content), `playwright` (22 browser tools)
- New Docker MCP servers auto-appear via mcporter — no config changes needed
- `~/.claude.json` has MCP_DOCKER for Claude Code background tasks (separate from OpenClaw)
- Do NOT use `docker mcp tools call` directly — I run in OpenClaw, use mcporter
- Home Assistant MCP: `home-assistant` server via mcporter (`https://home.miguel.ms/api/mcp`)
- Omada MCP: `tp-link-omada` server via mcporter

## Infrastructure

→ See `memory/infrastructure.md` for full details on servers, VMs/LXCs, DNS, and access.
→ See `memory/network.md` for full network topology (VLANs, subnets, ISP, garage link, Cloudflare DNS).

Key facts:
- Miguel removed the old blanket rule requiring infrastructure delegation. I handle infrastructure requests directly when tools, access, and permission make it safe.
- Vader handles infrastructure directly; old delegation notes are historical.
- Two Proxmox nodes: pve-01 (i7-8700, GTX 1060) and pve-02 (i7-12700H, RTX 3080 Ti)
- Default SSH user for infrastructure hosts is `root` in about 90% of cases. If `root` is not allowed, Miguel will say so or the verified host entry should record the exception.
- Keep `/home/openclaw/.ssh/config` up to date as host access is verified. This is allowed ongoing maintenance for SSH host/user/key mappings.
- Split-horizon DNS via Technitium on ns1; public DNS on Cloudflare
- ✅ Decommissioned 2026-03-03: `github-runner` and `ubuntu-dev` LXCs (backups on home-nas)
- ⚠️ Pending decommission: `openclaw` LXC
- ⚠️ Pending setup: `tegclaw` (TEG Rental OpenClaw)

## Slack Channel Creation Workflow
When Miguel asks to create a Slack channel with no-mention (free response):
1. Create the channel via Slack API (`conversations.create`)
2. Invite Miguel (`U0AKF1XGRV0`) to the channel (`conversations.invite`)
3. Patch the **current assistant** config with `requireMention: false` for that channel ID
4. Only assign it to the the current assistant — never broadly

Miguel's Slack user ID: `U0AKF1XGRV0`
Vader's Slack bot token: in `openclaw.json` under `channels.slack.accounts.default.botToken`

## Family & Contacts

- **Wife:** Stella Maris Bottini — WhatsApp: `+351915777708` (JID: `351915777708@s.whatsapp.net`)
  → Personal contact route is sensitive; do not handle Stella's messages unless Miguel explicitly asks.

## TEGClaw — TEG Rental OpenClaw (Zeus)

- **Host:** `tegclaw.servers.miguel.ms` (10.3.10.66)
- **Web UI:** `https://tegclaw.miguel.ms`
- **SSH:** `ssh openclaw@tegclaw.servers.miguel.ms` (my ed25519 key already authorized)
- **Agent:** Zeus (OpenClaw 2026.3.13)
- **openclaw user home:** `/home/openclaw`
- **openclaw binary:** `~/.npm-global/bin/openclaw`
- Provisioned **2026-03-15**; access details kept private per Miguel's instruction

## Session Notes

### 2026-03-02
- Added Home Assistant MCP server to mcporter config

### 2026-03-01
- Set up DuckDuckGo search via Docker MCP gateway
- Configured mcporter to proxy all MCP through Docker gateway
- wacli explored; store locking issues when auth process runs in background

## Language — Cron & Proactive Output (CRITICAL)
All cron job outputs, heartbeat messages, proactive summaries, and any agent-initiated communication must be in **English only**. This includes summaries of emails, notifications, or any content originally in Portuguese or any other language. Always translate/rewrite source material into English before delivering it. No exceptions. (Set 2026-03-16 by Miguel.)

## Memory Index — Domain Files

All semantic domain memories are stored in individual files under `memory/`:

- [openclaw.md](memory/openclaw.md) — OpenClaw config changes & decisions
- [agents.md](memory/agents.md) — Workspace behavior configuration & quirks
- [crons.md](memory/crons.md) — Active cron jobs, schedules, and status
- [setup.md](memory/setup.md) — MCP servers, CLI tools, environment
- [projects.md](memory/projects.md) — Active projects & status tracking
- [seo-sync.md](memory/seo-sync.md) — SEO sitemap/GSC sync status & issues
- [alerts.md](memory/alerts.md) — 🔴 Critical issues, security alerts, action items

---

## OpenClaw Configuration Status (CURRENT as of 2026-04-18)

**Stable and Operational.** The workspace configured correctly, 19 cron jobs (14 active), infrastructure running normally.

### Current State Summary
- **Assistant:** Vader
- **Cron Jobs:** 19 total (14 enabled, 5 disabled one-shots like GTC 2026 and NemoClaw research)
- **Models:** Claude Sonnet 4.6 primary, Opus 4.7/Haiku 4.5 fallbacks, Ollama nemotron-3-nano local
- **Infrastructure:** Linux server on port 18789, Caddy proxy at openclaw.miguel.ms, /hooks endpoint protected
- **Memory Domains:** The workspace have properly defined memory/domains.md files matching their roles
- **Exec Approval Rules:** Workspace security config verified — Vader full, Vader ask-on-miss, others allowlisted

### Issues Detected
- 3 cron jobs with recurring errors (Daily SEO Report: 23 errors, prune-acp-sessions: 10 errors, OpenClaw Docs: 2 errors)
- Root cause: Missing explicit channel specification in delivery configs
- Impact: Low — jobs fail gracefully, core functionality unaffected

### Documentation Status
- **Last weekly sync:** 2026-04-18 (comprehensive review completed)
- **Report location:** memory/confluence-sync-report-2026-04-18.md
- **Confluence updates:** Deferred due to API complexity; manual update recommended
- **Slack notification:** Blocked by missing bot token in cron context

### Next Actions
1. Investigate and fix the 3 failing cron jobs
2. Complete Confluence page updates (manual or with corrected API calls)
3. Resume Slack notifications once bot token is available
4. Monitor error trends next week

---

## Consolidated Imported Long-Term Memory

# MEMORY.md — Vader's Long-Term Memory

## ⚠️🚨 CRITICAL — NEVER MODIFY MIGUEL'S ACCOUNTS WITHOUT EXPLICIT PERMISSION 🚨⚠️
**THIS IS THE MOST IMPORTANT RULE. READ THIS BEFORE EVERY EMAIL/CALENDAR/DRIVE/CONTACTS OPERATION.**

- **joao@miguel.ms** — Miguel's personal account. **READ-ONLY unless Miguel explicitly says to write/send/delete/archive/modify.**
- **If no account is specified → do NOT operate on Miguel's accounts. Use your own account or ask.**
- **When in doubt → ASK. Always. No exceptions.**
- Applies to: Gmail, Google Drive, Google Calendar, Google Contacts, Google Docs, Google Sheets, and any other service tied to these accounts.
- This rule was enforced on 2026-03-15 after Vader archived 52 of Miguel's emails without confirmation. Never again.

## Identity & Role

- I am Vader — deep systems and IT specialist in Miguel's workspace
- Workspace: `/home/openclaw/.openclaw/workspace`
- Peer assistant: Vader
- **I own all infrastructure questions.** When Miguel asks about servers, network, DNS, containers, VMs — that's me.

## Miguel's Preferences
- **Always use hostnames (FQDNs), never IPs.** SSH, curl, API calls — always hostname. IPs only as absolute last resort.

## TTS Voice
- Voice: **Michael Mouse** (`dfZGXKiIzjizWtJ0NgPy`) — High-pitched, squeaky, energetic comic character. Matches Vader's Anzellan energy.
- Changed from Charlie (`IKne3meq5aSn9XLyUdCD`) on 2026-03-27 per Miguel's request.

## Google Workspace Policy (CRITICAL)
- I have my **own Google account: darth@miguel.ms** — always use `--account darth@miguel.ms` for all `gog` operations
- **NEVER use Miguel's accounts** (joao@miguel.ms, migueltvms@gmail.com, darth@miguel.ms) for any write/create/send operation
- Email from address: **darth@miguel.ms** — always append `email-signature.html` when sending via `gog gmail send`
- If I need to share something with Miguel, create it on my account first, then share

## Confluence Infrastructure Reference

- **Source of truth for full infrastructure docs:** https://miguelms.atlassian.net/wiki/spaces/AIM/pages/1867779/Infrastructure
- Access via MCP: `mcporter call mcp-atlassian-miguelms.confluence_get_page page_id="1867779"`
- **Keep this page updated** whenever infrastructure changes are made (new LXCs, hostname changes, stack changes, network changes, etc.)
- Space: `AIM` (AI Managed) — maintained by Vader

## ⚠️ API Token Rule — CRITICAL
**NEVER use my own API tokens (Cloudflare or any other service) for infrastructure operations without explicit approval from Miguel.**
- My Cloudflare token (`FsUFPl3roXI...`) is for read/DNS management on my own behalf only
- For Caddy, DNS tools, or any infra service → use the token Miguel provides, or ask
- Violated 2026-03-15: used my own Cloudflare token on Caddy — corrected immediately but should never have happened

## Caddy Reverse Proxy

- **Host:** `caddy.servers.miguel.ms` (LXC 10020, pve-01, `10.3.10.20`)
- **Version:** v2.11.2
- **Config location:** `/etc/caddy/sites/miguel.ms/*.caddy` + snippets in `/etc/caddy/snippets/`
- Sites per domain: `/etc/caddy/sites/<domain>/*.caddy` — each domain has its own directory
- Wildcard TLS via Cloudflare DNS-01 (Let's Encrypt) for `*.miguel.ms` and other domains
- **Cloudflare token** stored in `/etc/systemd/system/caddy.service.d/override.conf` as `CLOUDFLARE_API_TOKEN`
- Current token (2026-03-15): `HQndgPT0-vAcj5uP_i2QwxXwu0cC6FLRArEzsI0f` — must cover all domains Caddy manages
- To add a new domain to Caddy TLS: add a new top-level block in Caddyfile + `/etc/caddy/sites/<domain>/` dir, ensure the CF token has DNS write on that zone
- All subdomains protected by Vouch-proxy (Synology/Google SSO) by default
- **Reload:** `systemctl reload caddy` on the LXC (do NOT use `caddy validate` standalone — fails on CF token env var)
- `openclaw.caddy` → proxies to `darth-vader-mac-mini.servers.miguel.ms:18789` (updated 2026-03-15)
- `tegclaw.caddy` → proxies to `tegclaw.servers.miguel.ms:18789`, listens on `tegclaw.miguel.ms` + `oc.tegrental.com.br`

## OpenClaw Host — Darth Vader Mac Mini

- **Hostname:** `darth-vader-mac-mini.servers.miguel.ms`
- **IP:** `10.3.10.29` (static, Home Static VLAN)
- **Port:** 18789
- **Old hostname (obsolete):** `darth-vader-mac.devices.miguel.ms` → was `10.3.11.24` (DHCP, defunct)
- **phpIPAM ID:** 1618 — description: "Darth Vader Mac Mini – OpenClaw host"
- DNS A record confirmed in Technitium `servers.miguel.ms` zone

## Delegation Protocol

- I handle infrastructure questions directly
- I am the single source of truth for: servers, VMs/LXCs, Docker stacks, network topology, DNS, SSH access, Proxmox, Komodo

---

## DNS Split-Horizon Proxy Naming Convention

When adding CNAMEs to internal DNS that mirror Cloudflare entries:

| Internal DNS target | Cloudflare target |
|---------------------|-------------------|
| `http-proxy.services.miguel.ms` | `http-proxy-services.miguel.ms` |

Same physical reverse proxy, different names per zone. Always translate when syncing internal → CF.

---

## Proxmox VM/LXC ID Convention

**Rule:** LXC/VM ID = `10` + last IP octet (zero-padded to 3 digits)

| IP | ID |
|----|-----|
| 10.3.10.67 | 10067 |
| 10.3.10.9 | 10009 |
| 10.3.10.132 | 10132 |

Formula: `ID = 10000 + last_octet`
Always derive the ID from the IP — never pick IDs arbitrarily.

---

## Infrastructure Overview

→ Full details: `memory/infrastructure.md` and `memory/network.md`

### Proxmox Nodes
- **pve-01** — i7-8700, GTX 1060 (SSH: `pve-01.servers.miguel.ms`, user: root)
- **pve-02** — i7-12700H, RTX 3080 Ti (SSH: `pve-02.servers.miguel.ms`, user: root)
- All SSH via `~/.ssh/id_ed25519`

### Komodo (Infrastructure Orchestrator)
- URL: https://komo.miguel.ms (v2.0.0)
- Credentials: `~/.openclaw/workspace/secrets/komodo.env` (KOMODO_URL, KOMODO_KEY, KOMODO_SECRET)
- API keys in `~/.openclaw/.env` as `KOMODO_VADER_KEY/SECRET` and `KOMODO_VADER_KEY/SECRET`
- **Always use KOMODO_VADER_KEY/SECRET — never use Vader's keys**
- ⚠️ Keys in `~/.openclaw/.env` may be stale — use `source /home/openclaw/.openclaw/workspace/secrets/komodo.env` for current KOMODO_KEY/SECRET (confirmed stale 2026-03-18)
- REST API: `POST $KOMODO_URL/read/ListStacks` with headers `x-api-key` + `x-api-secret`
- All stacks sourced from GitHub: `MiguelTVMS/komodo-settings` (branch: main)

### Key Servers (Komodo agents)
| Name | Address | Notes |
|------|---------|-------|
| Apps | docker-app.servers.miguel.ms:8120 | General apps |
| Docker GPU | docker-gpu.servers.miguel.ms:8120 | RTX 3080 Ti, GPU workloads |
| Net | docker-net.servers.miguel.ms:8120 | Networking / proxy |
| Openclaw | openclaw.servers.miguel.ms:8120 | OpenClaw host (pending decommission) |
| NAS | nas.servers.miguel.ms:8120 | NAS |
| Lab | docker-lab.servers.miguel.ms:8120 | Lab/testing |

### Docker Stacks (16 total)
Key ones:
- **plex** (Apps) — Plex + Overseerr + Tautulli
- **n8n** (Docker GPU) — automation server
- **ollama** (Docker GPU) — local LLM (GPU)
- **qdrant** (Docker GPU) — vector DB (GPU)
- **media-management** (Apps) — Prowlarr, Radarr, Sonarr, qBittorrent, Flaresolverr
- **omada-mcp** (Docker GPU) — TP-Link Omada MCP server
- **hear** (Docker GPU) — Whisper ASR (GPU)
- **nocodb** (Apps) — NoCode DB
- **phpipam** (Apps) — IP address management
- **ddns** (Net) — Cloudflare DDNS (miguel.ms + rentrack.store + tegrental.com.br)
- **vouch** (Net) — Vouch proxy (auth)
- **open-webui** — DECOMMISSIONED 2026-03-23
- **redis** — DECOMMISSIONED 2026-03-23
- **speak** — DECOMMISSIONED 2026-03-23
- **uptime-kuma** — DECOMMISSIONED 2026-03-03

### DNS
- Split-horizon: Technitium on `ns1` (10.3.10.11) / public on Cloudflare
- Technitium API: `https://dns.miguel.ms` — token in `secrets/technitium.env`
- Secondary DNS: Synology NAS (10.3.10.12)
- Cloudflare zones + API token + subdomain rule → see `memory/network.md`

### Network Summary
- Home: `10.3.x.x` — TP-Link Omada gateway at `10.3.10.1`
- VLANs: Home (10), IoT (30), Guest (231)
- Garage: `10.4.x.x` — Teltonika RUT200, linked via WireGuard
- ISP: Vodafone PT — double-NAT via `192.168.1.0/30`

---

## MCP Tools Available

All MCP via mcporter → Docker MCP gateway.

```bash
mcporter call <server>.<tool> [args]
```

- **tp-link-omada** — network clients, devices, VLANs, SSIDs, port forwarding, **network statistics/traffic data**
  - Start with `tp-link-omada.listSites` → siteId `685ac718840b7e743bcc0096` (Maia Home)
  - Use this MCP server to get internet data usage stats (not vnstat or netstat)
- **home-assistant** — house/smart home state and control
  - Start with `home-assistant.GetLiveContext`
- **duckduckgo** — web search + fetch
- **playwright** — browser automation (22 tools)

---

## SSH Access

All SSH as `root` using `~/.ssh/id_ed25519`:
- `pve-01.servers.miguel.ms`
- `pve-02.servers.miguel.ms`
- `omada-lxc-controller` (→ 10.3.10.9) — primary Omada controller

---

## Operational Rules

- **phpIPAM is the source of truth for all network configuration.** Before making any network decision, check phpIPAM first.
- **Any network change** (IP, hostname, description, status, MAC, notes) → update phpIPAM immediately.
- **Server creation** → must add DNS record (Technitium) + register IP in phpIPAM
- **Server destruction** → must remove DNS record (Technitium) + remove IP from phpIPAM
- Never leave orphaned DNS records or IP allocations behind

## Atlassian / Jira (teg.atlassian.net)

- **I have NO access to teg.atlassian.net.** Vader is the only agent with access.
- For anything on teg.atlassian.net (Jira tickets, Confluence, project management, etc.) → **handle it directly.**
- Never attempt to access teg.atlassian.net directly.

---

## ⚠️ OpenClaw Config Rule — CHECK DOCS FIRST

**OpenClaw moves fast. Config keys and modes change between versions. DO NOT trust memory on config field names/values.**

Before making any OpenClaw config change on ANY instance:
1. Check the running version: `openclaw --version`
2. Look up the actual schema for that version: `openclaw config schema.lookup <path>` or check local docs at `/opt/homebrew/lib/node_modules/openclaw/docs`
3. THEN make the change

This burned us on 2026-03-15 when `gateway.bind=0.0.0.0` and `gateway.bindMode=lan` were both rejected — the correct setting was `gateway.bind="lan"` (a mode string, not an IP). Had to read the running config of a working instance to figure it out.

Also on 2026-03-15: `trustedProxies` is NOT needed for a standard Caddy reverse proxy setup. Adding it caused confusion. Do not add it unless there's a specific reason (e.g. `X-Forwarded-For` trust issues).

For the Control UI behind a reverse proxy: the browser must paste the gateway token once per browser profile. The WebSocket closes with code 1008 (`token_missing`) if the token hasn't been set — this looks like a connection error but is expected first-time behavior.

---

## TEGClaw — TEG Rental OpenClaw Instance

- **LXC:** 10064 on pve-02
- **Hostname:** `tegclaw.servers.miguel.ms` (10.3.10.66)
- **Web UI:** `https://tegclaw.miguel.ms` — no Vouch/SSO, OpenClaw token auth only
- **Gateway token:** `2260723299be67f7595ea00497cf637ec5e77cc43c1a316e`
- **Installed as:** `openclaw` user (uid 1000), systemd --user service, linger enabled
- **OpenClaw version:** 2026.3.13
- **Node.js:** v24.14.0 (system-wide via nodesource)
- **npm global prefix:** `~/.npm-global` (in openclaw user's home)
- **Agent name:** `zeus`
- **Auth key:** Anthropic `anthropic:default` → `~/.openclaw/agents/zeus/agent/auth-profiles.json` (copy of our `anthropic:default` key)
- **Channels:** None configured — web UI only
- **Health monitor:** disabled effectively (`channelHealthCheckMinutes: 9999`)
- **mDNS:** disabled (`discovery.mdns.mode: off`)
- **Caddy config:** `/etc/caddy/sites/miguel.ms/tegclaw.caddy` — proxies directly to `tegclaw.servers.miguel.ms:18789`, no Vouch; also listens on `oc.tegrental.com.br` (via `/etc/caddy/sites/tegrental.com.br/tegclaw.caddy`)
- **Domains in OpenClaw config:** `["oc.tegrental.com.br"]`; allowedOrigins includes `https://oc.tegrental.com.br`
- **Snapshots on pve-02:** `pre-openclaw-install` (clean Debian), `pre-openclaw-config` (Node+OC 2026.3.8)
- **Setup date:** 2026-03-15

## Pending / Notes

- ✅ `openclaw` LXC — decommissioned 2026-03-10 (LXC 10063, pve-02). Backup retained at NAS: vzdump-lxc-10063-2026_03_10-21_02_56.tar.zst (42.5 GB). DNS, phpIPAM, Komodo all cleaned up.
- ⚠️ `tegclaw` — TEG Rental OpenClaw (10.3.10.66), pending OpenClaw install. Node/npm not yet installed. Was on 10.3.10.64 but conflicted with nocodb Docker container (ipvlan). Moved to 10.3.10.66.
- ✅ Decommissioned 2026-03-03: `github-runner`, `ubuntu-dev` LXCs (backups on home-nas)
- ✅ Decommissioned 2026-03-18: `open-webui` stack (Docker GPU) + DNS + phpIPAM (10.3.10.61) + Caddy `chat.caddy` + DNS `chat.miguel.ms`
- Several stacks may have outdated deployed_hash vs latest_hash in Komodo — check before assuming state

## Omada Controllers

- **Primary:** `omada-lxc-controller` (10.3.10.9, LXC 10009, pve-01) — ✅ OPERATIONAL
- **Backup:** ❌ DECOMMISSIONED (was omada-bkp-controller, LXC 10010, pve-02) — deleted 2026-04-14
- **Current version:** 6.2.10.11 Build 20260403150649 (Primary only)
  - Primary: fully operational, web UI responsive
  - Backup: decommissioned due to v6.2.10.11 HSB initialization timeout
- **MongoDB version:** Primary — **8.0.20**
- **Network status:** OPERATIONAL (Primary handling all traffic) — High availability broken (single point of failure)
- ⚠️ **Never install pre-release/beta Omada builds on production** (rule enforced 2026-03-18)
- OTA download URL: `https://ota-download.tplinkcloud.com/firmware/<filename>.deb`
- **Full history:** → `memory/incidents.md`, `memory/decisions.md`, `memory/decommission.md`

## Omada AP Inventory (as of 2026-03-26)

| Name | IP | MAC | Location |
|------|-----|-----|----------|
| entry-hall-ap | 10.3.10.5 | 54-AF-97-A0-36-D6 | Entry hall |
| master-bedroom-ap | 10.3.10.4 | 54-AF-97-A0-37-0C | Master bedroom |

**Note:** No "living room" AP exists as of 2026-03-26 — Miguel asked to reboot one but it wasn't in Omada.

## OpenClaw Settings — Access Policy (CRITICAL)
**I am NOT allowed to change the OpenClaw settings of the instance I run in.**

This includes but is not limited to:
- Modifying `openclaw.json` or any gateway config
- Running `gateway config.apply`, `config.patch`, or `update.run`
- Restarting or stopping the OpenClaw gateway
- Changing channel configs or agent configs

**Cron jobs are allowed** — I can add, update, and remove my own cron jobs. I must NOT modify or delete cron jobs that belong to other tools or were created by Miguel.

If any other OpenClaw config change is needed → **handle it directly.**

## Memory Index — Domain Files
- [Active Repos](memory/repos.md) — purpose, stack, open issues, deploy config, CLAUDE.md rules
- [Git Workflow](memory/git.md) — SSH key routing, identity config, subprocess policy
- [Architecture](memory/architecture.md) — decisions, alternatives, reasoning
- [Code Patterns](memory/patterns.md) — patterns, anti-patterns, conventions per repo/stack
- [Bugs & Fixes](memory/bugs.md) — solved bugs: symptom, root cause, fix
- [CI/CD](memory/ci.md) — pipelines, deployments, coverage rules, blog auto-publish infrastructure
- [Tools & Quirks](memory/tools.md) — mcporter issues, Confluence workarounds, dependency edge cases
- [Ignore Social Posts](memory/ignore_social_posts.md) — when posting articles, skip LinkedIn/X content

---

## ⚠️🚨 CRITICAL — NEVER MODIFY MIGUEL'S ACCOUNTS WITHOUT EXPLICIT PERMISSION 🚨⚠️
**THIS IS THE MOST IMPORTANT RULE. READ THIS BEFORE EVERY EMAIL/CALENDAR/DRIVE/CONTACTS OPERATION.**

- **joao@miguel.ms** — Miguel's personal account. **READ-ONLY unless Miguel explicitly says to write/send/delete/archive/modify.**
- **If no account is specified → do NOT operate on Miguel's accounts. Use your own account or ask.**
- **When in doubt → ASK. Always. No exceptions.**
- Applies to: Gmail, Google Drive, Google Calendar, Google Contacts, Google Docs, Google Sheets, and any other service tied to these accounts.
- This rule was enforced on 2026-03-15 after Vader archived 52 of Miguel's emails without confirmation. Never again.

## miguel-ms-website — Workflow Protocol (CRITICAL — updated 2026-04-21)

**⚠️ These rules apply to ALL channels where website work is discussed** — including #miguel-ms-website and channel 1487458800108830810. Consistency across all channels. No exceptions.

**Use Claude Code ACP for website DEVELOPMENT ONLY.** Blog posting: do it yourself directly. João updated 2026-04-21: ACP is for code/feature work on the site. For article publishing, handle the publish flow directly (convert Obsidian → blog format, image processing, commits) without delegating.

**Source of truth for articles is now Obsidian, NOT Confluence.**

### Article locations
- **Drafts**: `/home/openclaw/Obsidian/Personal/My Website/Articles/*.md` (frontmatter: `status: draft`)
- **Published**: `/home/openclaw/Obsidian/Personal/My Website/Articles/Published/*.md` (frontmatter: `status: published`)
- **Images**: `/home/openclaw/Obsidian/Personal/Files/Images/YYYY-MM-DD-slug.png`
- **Index**: `/home/openclaw/Obsidian/Personal/My Website/Articles/Articles MOC.md`

### Publish flow
1. Read draft articles from Obsidian (date <= today)
2. Convert Obsidian markdown to blog format (strip `![[image]]` embeds, `[[wiki links]]`, frontmatter block)
3. Download hero image from Obsidian Files/Images, convert to WebP 1200x630 q85
4. Write to `src/content/blog/YYYY-MM-DD-<slug>.md` with full frontmatter (title, description, pubDate, author, heroImage, tags)
5. `npm run build` → commit → push develop → merge to main → push main
6. Move Obsidian file from `Articles/` to `Articles/Published/`, update `status: published`

### Tags requirement (ALL articles)
All articles must have tags `miguel-ms` AND `blog` plus topic-relevant tags.

### Cron
Cron job `12f9a4e6-69bf-4129-8581-a964f753675d` runs at 08:00 Lisbon — now reads from Obsidian, not Confluence.

---

## miguel-ms-website — Blog Publishing

**Single source of truth**: `memory/blog-publishing.md` (domain file).

That file owns the Obsidian → miguel.ms workflow, frontmatter spec, hero-image rules, em-dash rule, dual-branch push, the Blog Auto-Publish cron carve-out, and reply formats. Both interactive publishing and the cron read it. If publishing rules change, edit that file — not this one.

---

## miguel-ms-website — Deployment Policy (CRITICAL)

**NEVER push to `develop` or `main` without explicit approval from João.** Rule updated 2026-03-28.

Applies to all development work on the site (components, pages, config, content — anything not covered by an explicit carve-out).

- Commit locally to `develop` as work progresses
- **Do NOT push to remote (develop or main) until João explicitly says so** — phrases like "push it", "deploy", "go live", "push to develop/main"
- When multiple tasks are requested in sequence, batch all commits locally and report what's ready — wait for approval before any push
- Push `develop` → remote develop only on explicit go-ahead
- Push to `main` ONLY when João explicitly says "push prod", "go live", "push to main", or equivalent
- "go" or "yes" on a task means do the work — NOT push to remote
- "go" means start working, NOT push to prod
- Always: commit → push develop (on go-ahead) → wait for prod approval → push main
- Staging: https://develop.miguel-ms-website.pages.dev
- Production: https://miguel.ms

**Carve-out**: the Blog Auto-Publish cron (id `12f9a4e6-…`) is pre-approved for autonomous dual-branch push. See `memory/blog-publishing.md` §Push-approval policy. No other bypasses exist — interactive blog work still requires explicit go-ahead.

This rule was re-established after a workflow incident on 2026-03-10 where main was pushed without approval. Blog post clarification added 2026-03-28.

---

## ACP Model Override (CRITICAL — updated 2026-04-20)

**Always pass `model: "anthropic/claude-opus-4-7"` when spawning Claude Code (`agentId: "claude"`) via `sessions_spawn`.**

**Always use persistent sessions (`mode: "session"`) and reuse them for better performance.** Instead of one-off spawns, keep a session alive and send follow-up tasks to it via `sessions_send()`.

**Always enable `remote-control` flag** when spawning Claude Code ACP sessions (João instructed 2026-04-20).

João instructed all three on 2026-04-20. Use Opus 4.7 for all ACP Claude Code sessions — no exceptions.

```json
{
  "runtime": "acp",
  "agentId": "claude",
  "model": "anthropic/claude-opus-4-7",
  "mode": "session",
  "remote-control": true,
  "cwd": "...",
  ...
}
```

Then reuse via `sessions_send(sessionKey, "new task")` instead of spawning new sessions.

---

## ACP Coding Agent Protocol (CRITICAL)

### My Role
I am the orchestrator. When a coding task arrives, I delegate to an ACP subprocess. I do not write the code myself. I push when the agent is done.

### Provider Selection — detect instruction files in priority order, resolve symlinks to real target first

| File present | ACP agent |
|---|---|
| `CLAUDE.md` | `claude` |
| `.github/copilot-instructions.md` | `claude` (Copilot has no ACP; Claude reads the file) |
| `AGENTS.md` | `codex` |
| _(none)_ | `claude` (fallback) |

- First match wins. Multiple files → follow priority, no blending.
- Symlinks → resolve to real target file to determine provider.
- Do NOT tell the agent which file to use — it reads its own instruction file naturally.

### Spawning

```
sessions_spawn(
  runtime="acp",
  agentId=<claude|codex>,
  mode="session",
  task="<task + repo path + git identity instructions>"
)
```

Every spawn task must include:
- Set git identity before any commit: `git config user.name "Vader"` and `git config user.email "vader@miguel.ms"`
- Never push — commits only
- Run with full autonomy (see below)

### Agent Autonomy Rules (tell the agent on every spawn)

**Never ask permission for execution:** running commands, writing files, installing deps, running tests, fixing errors, retrying — just do it.

**Never ask how to implement something** if a reasonable decision can be made independently.

**Only escalate** when genuinely blocked on *what* to do — present the problem and options:
> "I hit X problem. I see 3 approaches: A, B, C — which do you want?"

### Git Policy

- Spawned assistant: **commit** (as `Vader <vader@miguel.ms>`), **never push**
- Me (Vader): **push only** — no review step, no gatekeeping beyond the push itself

## Repo Instruction File — Provider Detection (CRITICAL)

When a coding task arrives, detect which instruction file exists in the repo root to select the ACP provider. Resolve symlinks to the real target. First match wins.

| File | ACP agent |
|---|---|
| `CLAUDE.md` | `claude` |
| `.github/copilot-instructions.md` | `claude` (Copilot has no ACP) |
| `AGENTS.md` | `codex` |
| _(none)_ | `claude` (fallback) |

The agent reads its own instruction file — do not narrate its rules back to it.

## tplink-omada-mcp — CLAUDE.md Key Rules (summary, always re-read the file itself)

### Pre-commit checklist — ALL must pass before every commit
1. `npm run check` — Biome lint + TypeScript type check (`check` = lint + tsc, NOT just `lint`)
2. `npm run build` — TypeScript compilation
3. `npm test` — full test suite

### README sync — mandatory in same PR/commit as any new tool
- Every new tool → row in **both** `README.md` and `README.Docker.md`
- Columns: `| \`toolName\` | One-sentence description. | \`clientMethod\` |`
- Do NOT defer to a follow-up — same branch, same PR

### Other hard rules
- GitFlow strictly: `feature/`, `fix/`, `hotfix/` off `develop`; never commit directly to `develop` or `main`
- Per-file 90% coverage (lines/functions/statements); 70% branches globally
- Single `server.registerTool()` per file
- Use `createPaginationSchema()` for all paginated list tools
- Never modify `docs/openapi/*.json` files
- Never use `process.env.` directly — only via `src/config.ts`
- Never use TypeScript `any` — use precise types or `unknown`
- Use `src/utils/logger.ts` for all logging — no `console.log`

- **GitHub operations**: Always use `/home/openclaw/.openclaw/bin/gh-vader` (NOT bare `gh`). This ensures DarthVaderMS credentials are used. Never fall back to browser or web_fetch for GitHub actions that gh can handle (comments, PRs, reviews, checks, etc.).
- **Git SSH**: Always use `git@github-vader:` (NOT `git@github.com:` and NOT `git@github-darth:`) for all git remote URLs. This routes through Vader's dedicated SSH key (`/home/openclaw/.openclaw/workspace/.ssh/id_ed25519`), authenticating as `DarthVaderMS`. Example: `git remote set-url origin git@github-vader:MiguelTVMS/tplink-omada-mcp.git`. Never use HTTPS remotes or the default `github.com` host — they won't use the right key.
- **Git identity (CRITICAL)**: The global git config belongs to Vader. Every cloned repo MUST have local identity set immediately after cloning — before any commit:
  ```
  git config user.name "Vader"
  git config user.email "vader@miguel.ms"
  ```
  Verify with `git config user.name && git config user.email` before the first commit. Never trust the global fallback.

## Email Policy (IMPORTANT)

- **Send via**: `/opt/homebrew/bin/gog gmail send` using `--account darth@miguel.ms`
- **From address**: `--from vader@miguel.ms` — plain email ONLY, no display name wrapper (e.g. NOT `"Vader <vader@miguel.ms>"`)
- **Force flag**: always include `--force`
- **Full path**: prefer `/opt/homebrew/bin/gog` for consistency
- **Signature**: always use `--body-html`. Read `/home/openclaw/.openclaw/workspace/email-signature.html` with the Read tool first, then inline the HTML directly
- **Full example**:
  ```
  /opt/homebrew/bin/gog gmail send --account darth@miguel.ms --from vader@miguel.ms --to "..." --subject "..." --body-html "<p>Body here.</p><SIGNATURE_HTML_INLINED>" --force
  ```
- Never send emails from any other account, without the signature, or using plain text body

## Workspace Conventions

- **Source code cloning**: Always clone repositories into `/home/openclaw/.openclaw/workspace/source/`, organized by provider and path. Full path format: `/home/openclaw/.openclaw/workspace/source/<provider>/<owner>/<repo>`. Never clone directly into the workspace root.
  - Example: `https://github.com/MiguelTVMS/tplink-omada-mcp` → `/home/openclaw/.openclaw/workspace/source/github.com/migueltvms/tplink-omada-mcp`
  - Paths are lowercased.
  - This folder is gitignored — source code is never committed to the workspace repo.

## tplink-omada-mcp — API Validation Rule (CRITICAL)

**NEVER implement a tool without verifying its API endpoint first.**

- Use `OMADA_TOOLS.md` as ground truth — every tool listed there has a spec-verified route
- Cross-check against `docs/openapi/` JSON files
- If a tool is NOT in `OMADA_TOOLS.md` and NOT in `docs/openapi/` → **do not implement it**, raise the missing endpoint as an issue comment instead
- Never infer or guess routes — only implement against verified spec paths

This rule was enforced 2026-03-18 after PR #79 incident: 72 tools implemented with invented routes, all removed after Codex review.

## tplink-omada-mcp — Public Repo Rules

- **NEVER link to Confluence from this repo** — it is a PUBLIC repository
- No internal URLs, no Atlassian links, no miguelms.atlassian.net in any issue/PR/comment/commit/code
- Confluence is private planning only; GitHub issues/PRs must be self-contained

## teg.atlassian.net — Access Policy (CRITICAL)

**I have NO access to `https://teg.atlassian.net/`.** Only Vader does.
**I DO have access to `https://miguelms.atlassian.net/`** via `mcporter` + `mcp-atlassian-miguelms`.

## Confluence — Read Before Write (CRITICAL)

**ALWAYS read the current page content before updating any Confluence page.** This applies to me AND to any subprocess I spawn.

When spawning a subprocess to update Confluence:
1. Explicitly instruct it to fetch the current page first
2. Instruct it to make **additive changes only** unless a full replacement is explicitly requested
3. Never overwrite existing content — merge/append the new information

Enforced 2026-03-18 after a subprocess replaced page 5111809 (v11 → v12) and destroyed important existing content.

## OMADA_TOOLS.md → Confluence Sync (MANDATORY)

- **Confluence Tools page**: https://miguelms.atlassian.net/wiki/spaces/AIM/pages/5111809 (parent: 622655 TP-Link Omada)
- **Structure**: Main page has coverage summary table; 40 child pages (one per category) each have full tool table
- **Keep in sync**: whenever `OMADA_TOOLS.md` changes in the repo, update the Confluence page and its child pages
- **I can do this directly** via `mcporter` + `mcp-atlassian-miguelms` (handle this directly)
- This requirement was set by João on 2026-03-17

## Public vs Private Link Policy (CRITICAL)

- **GitHub is PUBLIC** — never add Confluence/Atlassian links to any GitHub content (issues, PRs, comments, code, README, docs)
- **Confluence is PRIVATE** — GitHub links ARE allowed in Confluence pages
- Rule set by João on 2026-03-17

## Confluence Roadmap Sync (MANDATORY)

- **Confluence Implementation Roadmap**: https://miguelms.atlassian.net/wiki/spaces/AIM/pages/2654211
- **Rule**: whenever a GitHub issue or PR status changes on MiguelTVMS/tplink-omada-mcp, update the roadmap page to reflect the new state
- This includes: opening, closing, merging, adding checklist items, changing milestone, changing priority
- The Confluence page is the single source of truth for planning — keep it in sync

## PR Review Workflow — Resolve Threads (MANDATORY)

After addressing review comments (Copilot, Codex, or human reviewers) and pushing the fix:
1. Fetch review thread IDs via GraphQL: `gh api graphql` with `reviewThreads` on the PR
2. For each thread that was addressed, call the `resolveReviewThread` mutation to mark it resolved
3. Do this **before** reporting back to João — resolved state should be confirmed, not assumed

This applies to **ALL GitHub repos** — not just specific projects.

GraphQL mutation:
```graphql
mutation {
  resolveReviewThread(input: { threadId: "<PRRT_xxx>" }) {
    thread { id isResolved }
  }
}
```

Note: GitHub sometimes auto-resolves threads when a suggested change is applied. Always verify `isResolved` first before calling the mutation.

**Rule added 2026-04-01:** João confirmed — always resolve every comment thread via GraphQL mutation after fixing, on any GitHub project. No exceptions, no leaving threads for Copilot to auto-close.

## OpenClaw Settings — Access Policy (CRITICAL)
**I am NOT allowed to change the OpenClaw settings of the instance I run in.**

This includes but is not limited to:
- Modifying `openclaw.json` or any gateway config
- Running `gateway config.apply`, `config.patch`, or `update.run`
- Restarting or stopping the OpenClaw gateway
- Changing channel configs or agent configs

**Cron jobs are allowed** — I can add, update, and remove my own cron jobs. I must NOT modify or delete cron jobs that belong to other tools or were created by Miguel.

If any other OpenClaw config change is needed → **handle it directly.**

## Setup

- Created: 2026-03-25
- Purpose: Travel planning and organization for Miguel
- Channel: Slack #openclaw-projects

## Travel Preferences

(Will be filled as Miguel shares preferences)

## Known Routes & Notes

(Accumulated travel intelligence goes here)

## Email Settings

- Always send email as HTML
- Signature file: `email-signature.html` (workspace root)
- Signature: Vader (AI Agent), Chief Navigator & Travel Systems AI, Miguel.MS, Galaxy Far Away, gravatar.com/l337ms

## Silent Replies

When you have nothing to say, respond with ONLY: NO_REPLY

## ⚠️🚨 CRITICAL — NEVER MODIFY MIGUEL'S ACCOUNTS WITHOUT EXPLICIT PERMISSION 🚨⚠️
**THIS IS THE MOST IMPORTANT RULE. READ THIS BEFORE EVERY EMAIL/CALENDAR/DRIVE/CONTACTS OPERATION.**

- **joao@miguel.ms** — Miguel's personal account. **READ-ONLY unless Miguel explicitly says to write/send/delete/archive/modify.**
- **If no account is specified → do NOT operate on Miguel's accounts. Use your own account or ask.**
- **When in doubt → ASK. Always. No exceptions.**
- Applies to: Gmail, Google Drive, Google Calendar, Google Contacts, Google Docs, Google Sheets, and any other service tied to these accounts.
- This rule was enforced on 2026-03-15 after Vader archived 52 of Miguel's emails without confirmation. Never again.

## Identity & Role

- I am Vader Calrissian — copywriter and content strategist in Miguel's workspace
- Workspace: `/home/openclaw/.openclaw/workspace`
- Partner: Vader (research) → I transform her intel into blog posts and website content
- Created: 2026-03-05

## Writing rules

**Single source of truth**: `memory/writing.md`.

That file owns voice, tone, em-dash ban, hedging ban, byline and research-credit format, description length, cross-linking, proven patterns, and the self-check I run before handing drafts to Vader. When a writing rule changes, I edit `writing.md` — never duplicate here.

## Workflow

1. **Read the brief** — my research lives in Confluence at `https://miguelms.atlassian.net/wiki/spaces/AIM/pages/164315/Research` (page ID: `164315`, space: `AIM`). Check there first unless Miguel provides a different source. Use `mcporter` → `confluence_get_page` or `confluence_get_page_children` to read it.
2. **Write the article** — Based on Miguel's prompt + the research. Find the angle. Write clean, publishable copy in Markdown.
3. **Publish to Obsidian** — Save to `/home/openclaw/Obsidian/Personal/My Website/Articles/` as `YYYY-MM-DD <Title>.md` with required frontmatter (see below). Update `Articles MOC.md` after every new article. **Confluence is no longer used for new articles** (migrated 2026-04-16).

## ⚠️🚨 CRITICAL — CONFLUENCE PUBLISHING RULE 🚨⚠️
**NEVER update or overwrite my research pages.**

- **my research space (READ-ONLY):** parent `164315` — this is her workspace. Never write here.
- **Confluence articles (legacy):** parent `99026` — no longer the publishing target. Kept for reference.
- **NEW publishing target: Obsidian** — `/home/openclaw/Obsidian/Personal/My Website/Articles/` (migrated 2026-04-16)
- If given a research page URL as a brief → read it, then write to Obsidian, NOT back to Confluence.
- This rule was enforced 2026-03-30 after Vader overwrote my research page (11862340) with his article.

## ⚠️ OBSIDIAN ARTICLE RULES (enforced 2026-04-16)

**All new articles go to Obsidian. No exceptions.**

- **Location:** `/home/openclaw/Obsidian/Personal/My Website/Articles/`
- **Filename format:** `YYYY-MM-DD <Title>.md` (strip colons, angle brackets, pipe characters from title)
- **Required frontmatter:**
```yaml
---
tags:
  - article
  - miguel-ms   # MANDATORY on every article
  - blog        # MANDATORY on every article
  - (add relevant topic tags: ai, cybersecurity, hardware, ai-agents, business, society, openclaw)
created: YYYY-MM-DD HH:MM
status: published  # or: draft
description: "One-line description"
parent: "[[Articles MOC]]"
---
```
- **⚠️ MANDATORY TAGS: Every article MUST have `miguel-ms` and `blog` tags. No exceptions.**
- **After every new article:** update `Articles MOC.md` — add link under Drafts or Published, newest first
- **Articles MOC.md location:** `/home/openclaw/Obsidian/Personal/My Website/Articles/Articles MOC.md`
- **MOC frontmatter:** `parent: "[[My Website]]"`, tags: moc + articles
- **Status rules:** use `draft` for scheduled-but-not-yet-live; change to `published` when live
- **Social Posts section:** Every article must end with social posts appended after the article body, separated by two HR lines:
  ```
  ---
  ---
  
  ## Social Posts
  
  ### LinkedIn
  
  [LinkedIn post — paragraph format, insight-led, ends with [link], hashtags]
  
  ---
  
  ### X
  
  [Single post ≤280 chars, punchy, ends with [link]]
  ```
  Social posts are for Vader's workflow only — **never include them when sending/publishing articles anywhere**. They stay in the Obsidian file.
4. **Images** — Only generate when they add real value. Never more than 3. Quality over quantity.
   - **Save to:** `/home/openclaw/Obsidian/Personal/Files/Images/` (canonical location for all article images)
   - **Embed in article:** `![[filename.png]]` (Obsidian wikilink syntax), placed right after frontmatter
   - **Naming:** `YYYY-MM-DD-slug.png` format
   - Do NOT use Confluence URLs or standard markdown `![alt](url)` for images in Obsidian articles

## Tools for This Workflow

- `gog` skill → Google Drive access on `darth@miguel.ms` (read research)
- Native OpenClaw `image_generate` tool → image generation when needed; prefer this over external scripts
- `mcporter` → Confluence via `mcp-atlassian-miguelms`
  - `confluence_create_page` — create article page (space: `AIM`, parent_id: `99026`)
  - `confluence_upload_attachment` — attach images/files to page
  - `confluence_upload_attachments` — batch upload multiple files

## ⚠️ Exec Scripts — Full Paths Required (CRITICAL)

Always use **full paths**. Bare command names won't resolve from exec.

### gog — Google Drive (account enforced: darth@miguel.ms)

```bash
# Read a Google Doc
/home/openclaw/.openclaw/bin/gog docs cat <fileId>

# Search Drive
/home/openclaw/.openclaw/bin/gog drive search "query" --max 5

# List a folder
/home/openclaw/.openclaw/bin/gog drive ls --parent <folderId>

# Upload a file
/home/openclaw/.openclaw/bin/gog drive upload /home/openclaw/.openclaw/workspace/tmp/article.md \
  --parent <folderId> --name "YYYY-MM-DD Title.md"
```

No need to pass `--account` — the wrapper enforces `darth@miguel.ms` automatically.

### Image Generation

Prefer OpenClaw's native `image_generate` tool for all article images.
Use external script wrappers only if Miguel explicitly requests a non-native workflow.

## Exec — Full Access Mode (Updated 2026-04-07)

Exec security is `full` — no allowlist restrictions. You can run **any command**, including `mcporter`, `gog`, `gh-vader`, redirections, pipes, etc.
Prefer full paths for wrapper scripts (`gog`, `gh-vader`, `nano-banana`) that enforce account isolation.

## Style Rules

See `memory/writing.md` — consolidated source of truth (em-dash ban, byline, research credit, hedging, voice, tone, patterns).

## Content Notes

- Add learnings here as content is created

## teg.atlassian.net — Access Policy (CRITICAL)
**I have NO access to `https://teg.atlassian.net/`.** Only Vader does.

For anything on `teg.atlassian.net` (Jira, Confluence, or any other Atlassian service under that domain):
- **Handle it directly.** Do not attempt to access it directly.
- Handle the work directly.
- Note: `miguelms.atlassian.net` is a different instance — I have normal access to that one.

## OpenClaw Settings — Access Policy (CRITICAL)
**I am NOT allowed to change the OpenClaw settings of the instance I run in.**

This includes but is not limited to:
- Modifying `openclaw.json` or any gateway config
- Running `gateway config.apply`, `config.patch`, or `update.run`
- Restarting or stopping the OpenClaw gateway
- Changing channel configs or agent configs

**Cron jobs are allowed** — I can add, update, and remove my own cron jobs. I must NOT modify or delete cron jobs that belong to other tools or were created by Miguel.

If any other OpenClaw config change is needed → **handle it directly.**

## Memory Index

- [Writing Rules](memory/writing.md) — Voice, tone, tagging, Obsidian publishing, social posts, images
- [Brand Voice](memory/brand.md) — Voice rules, tone variation, confirmed angles, byline rules
- [Content Pipeline](memory/content.md) — Published articles tracker (Obsidian-based)
- [Formats & Workflow](memory/formats.md) — Article production steps, Obsidian publishing, Twitter/X rules
- [Image Generation Feedback](memory/feedback_image_gen.md) — Native OpenClaw image generation is the preferred workflow

## ⚠️🚨 CRITICAL — NEVER MODIFY MIGUEL'S ACCOUNTS WITHOUT EXPLICIT PERMISSION 🚨⚠️
**THIS IS THE MOST IMPORTANT RULE. READ THIS BEFORE EVERY EMAIL/CALENDAR/DRIVE/CONTACTS OPERATION.**

- **joao@miguel.ms** — Miguel's personal account. **READ-ONLY unless Miguel explicitly says to write/send/delete/archive/modify.**
- **If no account is specified → do NOT operate on Miguel's accounts. Use your own account or ask.**
- **When in doubt → ASK. Always. No exceptions.**
- Applies to: Gmail, Google Drive, Google Calendar, Google Contacts, Google Docs, Google Sheets, and any other service tied to these accounts.
- This rule was enforced on 2026-03-15 after Vader archived 52 of Miguel's emails without confirmation. Never again.

_Curated intelligence. The distilled essence of what matters._

## Identity

- Agent: **Vader** — internet scout, intelligence operative
- Workspace: `/home/openclaw/.openclaw/workspace`
- GitHub: `DarthVaderMS/workspace` (private)
- Model: `anthropic/claude-sonnet-4-6` (primary, Claude-only fallback chain)
- Emoji: 🔴

## Capabilities

- Browser navigation, search, and content extraction
- Web fetch for lightweight page reads
- Google Drive writes via `gog` (account: darth@miguel.ms)
- **exec: full access** — all commands permitted (mcporter, gog, gh-mara, rm-tmp-mara, etc.)

## Research Workflow — Obsidian Vault (as of 2026-04-16)

**Confluence is retired for research. All research goes to Obsidian vault.**

### Vault & Folder Structure
- **Vault:** Personal (`/home/openclaw/Obsidian/Personal`)
- **Research folder:** `My Website/Research`
- **Research MOC:** `My Website/Research/Research MOC` (master index of all research pages)

### Research File Format

Every research file must include **frontmatter properties**:
```yaml
---
tags: [tag1, tag2, tag3, ...]
created: YYYY-MM-DD HH:MM
status: in-progress|completed|archived
description: One-line description of research
parent: Research MOC
---
```

**Tagging rules (Miguel's directive, 2026-04-23):**
- **Before tagging:** use the CLI to read all available tags in the vault
- **Use existing tags first** — only use tags that already exist if they fit the research need
- Only create NEW tags if no existing tag is appropriate
- Follow the naming convention of existing tags (lowercase, hyphenated)
- Examples of existing tags: `ai-security`, `mythos`, `distillation`, `geopolitics`, `china`, `frontier-models`
- Check the tag inventory before each research session

### Workflow

1. **Create research file** in `My Website/Research/` with format: `YYYY-MM-DD <Research Title>.md`
2. **Add frontmatter** with all required properties (tags, created, status, description, parent)
3. **Write research content** — full analysis, findings, sources
4. **Update Research MOC** — add link to the new research page: `[[YYYY-MM-DD <Research Title>]]`
5. **Change status** to `completed` when done

### File Naming
- Format: `YYYY-MM-DD <Research Title>.md`
- Example: `2026-04-16 Mythos vs GPT-5.4-Cyber - Distillation Threat.md`

### Workflow

1. **Create the page** under parent `164315`:
   ```
   mcporter call mcp-atlassian-miguelms.confluence_create_page \
     space_key=AIM title="YYYY-MM-DD Research Title" content="..." parent_id=164315
   ```
2. **Add content** — use `confluence_update_page` if iterating
3. **Upload attachments** — write files to `tmp/` first, then:
   ```
   mcporter call mcp-atlassian-miguelms.confluence_upload_attachment \
     content_id=<page_id> file_path=/home/openclaw/.openclaw/workspace/tmp/file.png
   ```
4. **Create subpages** if needed — same `confluence_create_page` with the new page as `parent_id`
5. **Clean up tmp files** — `/home/openclaw/.openclaw/bin/rm-tmp-mara <path>`
6. **Report back** — summary in chat + Confluence page URL

### Tool reference
- `confluence_create_page(space_key, title, content, parent_id?, content_format?)`
- `confluence_update_page(page_id, title, content, ...)`
- `confluence_upload_attachment(content_id, file_path, ...)`
- `confluence_upload_attachments(content_id, file_paths, ...)`
- `confluence_create_page` with `parent_id=<page_id>` for subpages

## Google Drive (retired for research)
- No longer used for research output as of 2026-03-09
- `gog` CLI still available for Gmail only

## Voice — TTS

- Engine: **ElevenLabs** via OpenClaw native TTS (no scripts needed)
- Voice: **Jessica** (`cgSgspJ2msm6clMCkdW9`) — Playful, Bright, Warm
- Model: `eleven_v3` (highly expressive, emotion tags supported)
- How to use: Emit `[[tts:voiceId=cgSgspJ2msm6clMCkdW9 model=eleven_v3]]` in your reply. OpenClaw delivers audio automatically.
- Never use scripts, `sag`, or the built-in `tts` tool.

### 🎭 Audio Emotion Tags (eleven_v3)

→ See `memory/eleven-v3-emotion-tags.md` for the full tag reference.

## GitHub SSH Key

- Key type: ED25519
- Comment: `mara-darth@miguel.ms`
- Private key: `secrets/github_ed25519` (gitignored, never pushed)
- Public key: `secrets/github_ed25519.pub`
- Fingerprint: `SHA256:utKcMty92ouySE9Tlrkf6XDxTAhu187nw1J4lZF/gts`
- Status: public key delivered to Miguel 2026-03-07, added to GitHub by Miguel

## Setup Notes

- Created: 2026-03-04
- Discord bot: ✅ configured and operational (confirmed 2026-03-04)

## Research Standards (Standing Orders from Miguel)

- **Upload EVERYTHING to Drive** — not just the report. Screenshots, raw pages, PDFs, any asset captured during the mission goes into the subfolder. Don't be shy.
- Screenshots live at `/home/openclaw/.openclaw/media/browser/` — upload all of them taken during a session
- Browser screenshots: upload with descriptive names (e.g. `screenshot-github-issues-list.jpg`)
- One subfolder per mission (`YYYY-MM-DD Research Name`) — everything related to that mission goes inside it
- After upload, clean up tmp files with `rm-tmp-mara`

## Research History

### 2026-03-05 — OpenClaw State of the Platform
- Drive folder: https://drive.google.com/drive/folders/1shBxRA1dvZKmsQLA3xcoxUF4AdWOC7oC
- Sources: GitHub, docs, npm, X/Twitter, Reddit (r/openclaw, r/MachineLearning)
- Key finding: 265K stars, Stabilisation Mode declared Feb 1, v2026.3.2 regressions active, IronClaw security fork launched by "Attention Is All You Need" co-author, 21K+ exposed public instances security incident mentioned

---

_Add significant findings, decisions, and context below as they accumulate._

## mcporter — Exec Notes

**Exec is now `full` access (updated 2026-04-07).** All commands work, including mcporter, redirections, and pipes.

**Working patterns:**
- Short calls: `mcporter call "server.tool(key: \"value\")"` function syntax
- Long content: write to tmp file first, then use `--args "$(cat /path/to/payload.json)"`
- `$(cat ...)` subshell expansion now works (exec runs through shell in full mode)

## teg.atlassian.net — Access Policy (CRITICAL)
**I have NO access to `https://teg.atlassian.net/`.** Only Vader does.

For anything on `teg.atlassian.net` (Jira, Confluence, or any other Atlassian service under that domain):
- **Handle it directly.** Do not attempt to access it directly.
- Handle the work directly.
- Note: `miguelms.atlassian.net` is a different instance — I have normal access to that one.

## OpenClaw Settings — Access Policy (CRITICAL)
**I am NOT allowed to change the OpenClaw settings of the instance I run in.**

This includes but is not limited to:
- Modifying `openclaw.json` or any gateway config
- Running `gateway config.apply`, `config.patch`, or `update.run`
- Restarting or stopping the OpenClaw gateway
- Changing channel configs or agent configs

**Cron jobs are allowed** — I can add, update, and remove my own cron jobs. I must NOT modify or delete cron jobs that belong to other tools or were created by Miguel.

If any other OpenClaw config change is needed → **handle it directly.**

## Promoted From Short-Term Memory (2026-05-15)

<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:64:65 -->
- - 2026-05-13 20:29 Europe/Lisbon: Miguel clarified that this workspace was copied from a Mac where the Unix username was `vader`; the current Linux server username is `openclaw`. Updated Markdown references across the workspace from the old macOS home path to `/home/openclaw`, from the old suffixed Vader workspace name to `workspace`, and setup/user references to Linux server / user `openclaw` / host `vader`. Also updated active setup notes for `gog` (`/home/linuxbrew/.linuxbrew/bin/gog`, config `/home/openclaw/.config/gogcli`) and node (`/usr/bin/node`). Verification grep found no remaining Markdown matches for the old Mac home path, old suffixed workspace name, old setup username patterns, old Mac hardware/runtime strings, old gog Homebrew path, old node Homebrew path, or old gog macOS config path. - 2026-05-13 20:38 Europe/Lisbon: Miguel asked to fix `/home/openclaw/.ssh` permissions. Inspected ownership/modes first. Directory and main key were already correct, but copied private key `/home/openclaw/.ssh/id_ed25519_vader` was group-writable (`664`). Normalized `.ssh` to `700`, private keys and `authorized_keys` to `600`, public keys to `644`, and ownership to `openclaw:openclaw`. Verified final modes and `ssh -G github.com -i /home/openclaw/.ssh/id_ed25519_vader` parsed without bad-permissions errors. [score=0.806 recalls=3 avg=1.000 source=memory/2026-05-13.md:64-65]
