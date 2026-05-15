# Old Workspace Memory Import Report — 2026-05-15

## Import Summary

- Imported old workspace `MEMORY.md` files and `memory/**/*.md` files into the current workspace.
- Merged date-suffixed daily fragments into canonical `memory/YYYY-MM-DD.md` files.
- Rebuilt `memory/domains.md` with 46 domain entries.
- Created backup before the completed import: `.migration-backups/old-agent-memory-import-20260515T143703Z`.
- Source archive under `old_agents/` was not modified.

## Normalization

- Active memory was normalized into the current single-assistant worldview.
- Old workspace names, old agent names, old account aliases, and old `workspace-*` paths were removed from active `MEMORY.md` and `memory/**/*.md`.
- Old source files in `old_agents/` still contain their original names and paths by design; they are archival input, not active memory.
- Some generic uses of "agent" remain where they describe OpenClaw config fields, ACP/Codex/Claude mechanics, or industry "AI agent" topics.

## Reindex Result

- Command run: `HOME=/home/openclaw openclaw memory index --force`.
- Result: index updated for `main`.
- Current indexed scope: 203 memory files and 12 session files; 215 total files/chunks.
- Current backend: `qmd`.
- Final memory status: `dirty: false`.
- Verification searches returned imported/current facts for Proxmox HA, `tplink-omada-mcp`, and the Milan/Florence trip.

## Reindex Caveats

- `qmd` is installed at `/home/openclaw/.npm-global/bin/qmd` and reports version `2.1.0`.
- `qmd` initially failed because its bundled `better-sqlite3` native module was built for a different Node ABI; `npm rebuild better-sqlite3 --prefix /home/openclaw/.npm-global/lib/node_modules/@tobilu/qmd` fixed the CLI/runtime mismatch.
- `qmd` semantic vectors are still unavailable, so semantic/vector recall remains degraded; file indexing and keyword retrieval are clean.

## Available Now

- OpenClaw CLI: `/home/openclaw/.npm-global/bin/openclaw`.
- `qmd`: `/home/openclaw/.npm-global/bin/qmd` (`2.1.0`).
- Google Workspace CLI: `/home/linuxbrew/.linuxbrew/bin/gog`.
- GitHub CLI: `/home/linuxbrew/.linuxbrew/bin/gh`.
- `nano-pdf`: `/home/openclaw/.local/bin/nano-pdf`.
- `goplaces`: `/home/linuxbrew/.linuxbrew/bin/goplaces`.
- `wacli`: `/home/linuxbrew/.linuxbrew/bin/wacli`.
- `ffmpeg`: `/home/linuxbrew/.linuxbrew/bin/ffmpeg`.
- Active workspace skills include: `cloudflare-dns`, `komodo`, `phpipam`, `technitium-dns`, `teltonika-rut200`, `github`, `gog`, `goplaces`, `nano-pdf`, `wacli`, `weather`, `video-frames`, `tmux`, `taskflow`, `session-logs`, and browser automation.
- MCP config currently lists: `home-assistant`, `tp-link-omada`, `mcp-atlassian-miguelms`, and `mcp-atlassian-velcra`.

## Missing Or Stale Tools From Imported Notes

| Tool or integration | Status | Impact | Recommended action |
|---|---|---|---|
| `mcporter` CLI | Retired / no longer required | Old notes using direct `mcporter call ...` are stale. Native OpenClaw MCP now covers the relevant integrations. | Do not restore `mcporter` by default; update workflows to use native MCP. |
| Semantic/vector memory support | `qmd` active, semantic vectors unavailable | Vector recall is degraded, but the QMD file index is clean and current. | Install/fix the vector/embedding dependency expected by current OpenClaw/QMD, then rerun `openclaw memory index --force`. |
| `mcp-atlassian-teg` | Resolved — configured in native OpenClaw MCP | TEG Atlassian access is present as native MCP via `uvx mcp-atlassian`. | Use native MCP tooling; no missing-tool action needed. |
| Obsidian tooling | Resolved — `obsidian-cli` and `ob` are installed and configured | Current default vault resolves to `/home/openclaw/vaults/personal`; headless sync uses `ob`. Old `/Users/vader/Obsidian/Personal` paths are still stale. | Use the configured Linux vault path and current tools; no missing-tool action needed. |
| `summarize` | Missing and skill disabled | Old research notes use `summarize` for URLs, PDFs, and YouTube. | Install `summarize` or replace with `web_fetch`, browser, `pdf`, and current model summaries. |
| GitHub account wrappers | Retired / no longer required | Imported notes mention dedicated wrapper binaries such as `gh-vader`, but the current workflow is plain `gh`. | Use plain `gh`; do not restore old wrapper scripts by default. |
| Safe-delete wrappers | Missing: `rm-tmp`, `trash`, old workspace-specific variants | Old deletion workflows reference wrappers that no longer exist, and this workspace is on Linux. | Install/configure a recoverable Linux trash CLI or add a single Linux-safe tmp deletion wrapper if Miguel wants that guardrail. |
| `nano-banana` image workflow | Retired / no longer required | Old image-generation notes reference a macOS script path. Current workflow uses native OpenClaw image generation. | Use native `image_generate`; do not restore `nano-banana` / `nano-banana-pro`. |
| Docker CLI | Missing | Old Docker MCP gateway commands and local Docker checks will fail from this host. | Install Docker/Podman CLI if local container operations are expected, or keep using remote Komodo/SSH. |
| Discord channel integration | Config missing according to skill status | Old notes contain Discord routing/cron delivery details; current config audit shows only WhatsApp configured, and Discord skill is disabled. | Re-add Discord channel config if Discord delivery should continue. |
| Slack integration | Config missing according to skill status | Old Slack channel/channel-creation notes are stale; Slack skill is disabled. | Re-add Slack config only if Slack should be active again. |
| Google Flights MCP | Resolved — configured as native MCP server `fli` via `uvx --from flights[mcp] fli-mcp` | Flight search automation is now present through native MCP config. | Use native MCP tooling; no missing-tool action needed. |
| Homebrew macOS paths | Stale | Old notes reference `/Users/vader`, `/opt/homebrew`, and `/usr/local/bin`. | Prefer Linux paths under `/home/openclaw`, `/home/linuxbrew/.linuxbrew`, and `/home/openclaw/.openclaw/workspace`. |

## Current OpenClaw Health Notes

- Installed OpenClaw CLI reports version `2026.5.12`.
- `openclaw channels status --json` and `openclaw status --json` fail from this shell with gateway `unauthorized`; config-only channel output shows WhatsApp configured. The live webchat session is working, so this is a CLI auth/status limitation to fix separately.
- `openclaw plugins list --json` reports `canvas` loaded but missing required deps: `@a2ui/lit`, `@lit/context`, and `lit`.
- Disabled/missing optional skills from the current install include macOS-only or unconfigured tools such as `apple-notes`, `apple-reminders`, `bear-notes`, `imsg`, `peekaboo`, `things-mac`, `notion`, `trello`, `xurl`, `openai-whisper`, and `openai-whisper-api`.

## Recommended Follow-Up

1. Decide whether semantic/vector memory support is needed beyond the now-working QMD file index.
2. Replace stale direct `mcporter` CLI references with native OpenClaw MCP workflows.
3. Re-add only the external channels Miguel still wants: likely Discord first, Slack only if still used.
4. Define the Linux Obsidian vault path or retire those workflows from active memory.
5. Add `mcp-atlassian-teg` if TEG Atlassian work should remain accessible from this workspace.
