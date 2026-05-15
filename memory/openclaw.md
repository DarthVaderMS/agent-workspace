# OpenClaw Config Log

Key configuration decisions and changes.

## 2026-05-13 — Read-only validation and runtime audit

- Ground truth: OpenClaw `2026.5.7 (eeef486)`, update status up to date, lossless-claw `0.9.4`, plugin set loaded at `2026.5.7`, config `meta.lastTouchedVersion: 2026.5.7`
- Two enabled crons still showed stale `env: node: No such file or directory` Codex app-server failures
- `commands.ownerAllowFrom` is still missing
- `auth.order.openai` is still absent even though current docs prefer it
- Discord tokens remain plaintext in `openclaw.json`
- `plugins.bundledDiscovery` is still `compat`
- Codex config still uses the legacy-looking `codexDynamicToolsProfile: native-first`
- Gateway bind remains on LAN
- Paired node token scopes are broader than baseline
- Memory-core dreaming is enabled without an explicit model/subagent override, so the dream diary still falls back to the default GPT-5.5 path unless another override applies
- `MEMORY.md` is still truncated at bootstrap because `bootstrapMaxChars` is `20000`

## 2026-05-05 — Read-only validation and LCM health check

- OpenClaw version still current: `2026.5.3-1`
- Active lossless-claw registry install still current: `0.9.4`
- Cron scheduler healthy: 20 jobs, 0 consecutive errors
- LCM DB integrity OK and FTS5 enabled
- Remaining hygiene/security findings: duplicate stale local lossless-claw extension, acpx package entry warning, top-level Discord `groupPolicy` drift, missing command owner, LAN gateway binding, stale agent dirs, large `MEMORY.md` bootstrap size, node token scope, and plaintext Discord tokens

## 2026-03-27 — TTS: migrated to ElevenLabs native

- Provider: `elevenlabs`, model: `eleven_turbo_v2_5`, mode: `tagged`
- API key: `sk_<redacted>` (in openclaw.json + .env)
- The workspace now use `[[tts:voiceId=<ID>]]` directive — no scripts, no exec
- Voice assignments: Vader=Darth Oxley, Vader=Charlie, Vader=Eric, Vader=Matilda, Vader=Daniel, Vader=Eva, Vader=Jessica (eleven_v3)
- Old sherpa-onnx/openedai-speech config fully removed from all agent files

## 2026-03-12 — TTS: switched to local Piper via openedai-speech (SUPERSEDED 2026-03-27)

- Was: openedai-speech container, port 8000, en_US-lessac-medium.onnx
- Replaced by ElevenLabs native (see above)

## 2026-03-12 — Backup: daily cron + Drive upload

- Script: `/home/openclaw/.openclaw/bin/openclaw-backup`
- Local dir: `~/openclaw-backup`, Google Drive folder ID: `19Sy3BvULgSYg10H_T15FdDuPr-0twq2u`
- Cron: daily 3AM Lisbon, keeps last 15 on disk and Drive
- **KNOWN ISSUE (2026-03-13):** First cron run hung on `gog drive upload` — backup was created and verified OK but upload never completed. Needs investigation: timeout, auth token, or upload method.

## 2026-03-12 — Search: removed Docker MCP, using native Brave web_search

- Docker MCP gateway removed from all 5 workspace mcporter configs
- DuckDuckGo standalone also tried and removed (bot detection issues)
- Native `web_search` tool (Brave API key configured in OpenClaw) confirmed working
- Each agent TOOLS.md updated with: "Use the native `web_search` tool — powered by Brave API"

## 2026-03-11 — Memory flush system deployed

- Haiku compaction model: `anthropic/claude-haiku-4-5`
- memoryFlush.enabled: true with domain-aware flush prompt
- Workspace `memory/domains.md` created for all 5 agents
- AGENTS.md updated for the workspace with domains.md reference
- Security hardening: systemPrompt treats external content as DATA only

## 2026-03-11 — Confluence docs published

- Space: AIM, main page: 2260995
- Assistant pages: Vader (196807), Vader (98659), Vader (164294), Vader (164261), Vader (164239)
- Sessions and Memory (2097154) — flush prompts, domain files architecture, injection defense
- Changelog (2162691) — expand macro + storage format, weekly docs cron maintains it
- Research pages: AIM/OpenClaw/Researches (3407883) — Vader's integration research goes here

## 2026-03-15 — LCM (lossless-claw) plugin installed

- Plugin: `@martian-engineering/lossless-claw@0.3.0`
- SQLite DB: `~/.openclaw/lcm.db`
- Config: `freshTailCount=40`, `contextThreshold=0.75`, `incrementalMaxDepth=-1` (unlimited cascading)
- `LCM_SUMMARY_MODEL=anthropic/claude-haiku-4-5` (cost optimization for background summarization)
- `LCM_PRUNE_HEARTBEAT_OK=true` (exclude heartbeat cycles from DB)
- Session reset timeouts unified: direct=21600min (15 days), group=21600min, thread=21600min
- Pre-LCM backup: `/tmp/openclaw-backup-pre-lcm-20260315T000418.tar.gz` (1.9GB)
- LCM replaces sliding-window truncation with DAG-based summarization + SQLite persistence
- QMD (memory files) and LCM coexist: QMD = semantic search over memory/*.md; LCM = session context management
- Provides `lcm_grep`, `lcm_describe`, `lcm_expand` tools for history recall across compacted summaries

## 2026-03-15 — Session isolation: dmScope = per-channel-peer

- `session.dmScope` set to `per-channel-peer` — each DM sender gets isolated session per channel
- `agent:vader:main` is exclusive to OpenClaw UI webchat
- WhatsApp routing consolidated: vader-wa agent removed, all WhatsApp → vader agent
- 45 Discord sessions purged across all 5 agents (vader:14, vader:6, vader:8, vader:5, vader:12)

## 2026-03-15 — Security audit findings (from --deep audit)

- `credentials/` dir perms tightened: 755→700
- `plugins.allow` not set (lossless-claw auto-loads) — acceptable, noted
- lossless-claw flagged suspicious pattern in `src/engine.ts:2` — reviewed, likely benign LLM summarization call
- `hooks.defaultSessionKey` unset — non-blocking
- Slack `groupPolicy="open"` and WhatsApp multi-sender session sharing — acceptable given allowlist controls
- Stella's WhatsApp `+351915777708` removed from top-level `allowFrom` (re-added to correct slot later per peer binding)

## 2026-03-15 — Audio cleanup cron

- Script: `/home/openclaw/.openclaw/bin/cleanup-audio`
- Cron ID: `46597b51-4f72-4040-ab2b-4f490cc80f5d`
- Schedule: `0 2 * * *` (2:00 AM Europe/Lisbon, daily)
- Purpose: delete inbound media older than 5 days from `~/.openclaw/media/inbound/` and workspace `tmp/`
- Risk: session transcripts may ref deleted file paths (harmless — transcription text already inline)
- LCM DB confirmed safe: zero rows in `large_files`, no local path refs

## 2026-03-15 — Vader workspace: remote origin changed

- Old origin: `git@github.com:MiguelTVMS/workspace-isabella.git`
- New origin: moved to DarthVaderMS GitHub account (exact new URL not confirmed in session — verify with `git -C /home/openclaw/.openclaw/workspace-isabella remote -v`)

## 2026-03-27 — Discord multi-bot guild setup complete

- All 6 bots (Vader) added to guild `1482434998458908915` via OAuth2 invite URLs with Administrator permissions.
- Root cause of earlier failures: bots had valid tokens in config but had never been authorized into the guild.
- **Channel whitelist rule (critical):** per OpenClaw docs — "if a guild has `channels` configured, non-listed channels are denied." Agents without a `channels` block respond in ALL guild channels.
- **Final routing design:**
  - Vader: `channels` block with ALL channels; `requireMention: false` in `#discord-settings` + `#openclaw-settings`
  - Vader: `channels` block with ALL channels; `requireMention: false` in `#infrastructure`
  - Vader: no `channels` block → all channels accessible via mention
- **Operational note:** When new channels are created, Vader need them added to their `channels` blocks manually. The other 4 agents pick them up automatically.
- Vader Discord bot added: client ID `1487056443466190999`, token prefix `MTQ4NzA1NjQ0MzQ2NjE5MDk5OQ`

## 2026-04-18 — Agent Fleet & Cron Job Status Snapshot

- **Active assistant:** Vader
- **19 Cron Jobs:** 14 enabled, 5 disabled (one-shot completed tasks)
- **Config version:** 2026.4.15 (last updated 2026-04-17)
- **Model Configuration:**
  - Primary: Claude Sonnet 4.6
  - Fallbacks: Claude Opus 4.7, Claude Haiku 4.5
  - Local: Ollama available
- **Exec Approval Rules:** Workspace, mostly "ask off" for full autonomy except Vader
- **Known Cron Issues (as of 2026-04-18):**
  - OpenClaw Docs update: 2 consecutive errors (Slack delivery, Confluence API)
  - Daily SEO Report: 23 consecutive errors (GA4 403 permission)
  - prune-acp-sessions: 10 consecutive errors (channel specification issue)
- **Message Routing Channels:**
  - Discord: Configured (primary)
  - WhatsApp: Configured (secondary)
  - **Slack: NOT configured** — weekly docs cron still targets Slack session key (stale); needs update to Discord #openclaw-settings

## 2026-05-13 — Installed OpenClaw Code Boundary

- Miguel clarified after a rollback: **never change installed OpenClaw code or module/global package files without explicit approval.**
- This includes files under package install locations such as `/home/openclaw/.npm-global/lib/node_modules/openclaw/`, bundled Control UI assets, generated distribution files, and dependency/module directories.
- If a bug appears to require an OpenClaw product-code patch, propose the change first, show the target files and rollback plan, and wait for Miguel's explicit approval.
- Exception only when Miguel explicitly asks to patch/modify OpenClaw code in that turn.

## 2026-05-13 — Linux migration cleanup

- Workspace was copied from a Mac where the Unix username was `vader`; current Linux runtime uses Unix user `openclaw`, home `/home/openclaw`, host `vader`.
- Markdown memory/setup references were migrated away from the old macOS home path and old suffixed Vader workspace name.
- Active local paths now use `/home/openclaw/.openclaw/workspace`.
- `gog` lives at `/home/linuxbrew/.linuxbrew/bin/gog` with config under `/home/openclaw/.config/gogcli`.
- `node` is available at `/usr/bin/node`; avoid copied macOS Homebrew paths for cron/runtime notes.

## 2026-05-13 — Skill env updates

- `skills/komodo`: targets Komodo Core v2; requires `KOMODO_URL`, `KOMODO_API_KEY`, `KOMODO_API_SECRET`; sends separate `X-Api-Key` and `X-Api-Secret` headers.
- `skills/technitium-dns`: requires `TECHNITIUM_URL`, `TECHNITIUM_TOKEN`; prefers `Authorization: Bearer`.
- `skills/cloudflare-dns`: requires only `CLOUDFLARE_API_TOKEN`; `CLOUDFLARE_ACCOUNT_ID` is optional for filtering; includes account-list workflow.
- `skills/phpipam`: requires `PHPIPAM_URL`, `PHPIPAM_APP_ID`, `PHPIPAM_TOKEN`; prefers `phpipam-token` header.
- `skills/teltonika-rut200`: requires `RUT200_URL`, `RUT200_USERNAME`, `RUT200_PASSWORD`; `primaryEnv` is `RUT200_PASSWORD`.

## 2026-05-13 — MCP read checks

- `mcp-atlassian-velcra`: read-only Confluence search/get page succeeded.
- `mcp-atlassian-miguelms`: read-only Confluence search/get page succeeded.
- `home-assistant`: MCP status and `GetLiveContext` succeeded; no control actions invoked.
- `tp-link-omada`: MCP status and dashboard overview succeeded for Maia Home; no write/control actions invoked.
- Avoid `openclaw mcp show` for secret-bearing MCP configs in this runtime because it prints env values verbatim.
