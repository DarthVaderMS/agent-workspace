# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Obsidian CLI (All Vault Operations)

**When Miguel asks you to work with Obsidian:**

1. **Always use the CLI** — `/usr/local/bin/obsidian` — not the desktop app or web UI
2. **Default vault is "Personal"** — `/home/openclaw/Obsidian/Personal` — unless Miguel explicitly specifies a different vault
3. **Common operations:**
   - `obsidian vault list` — list all vaults
   - `obsidian vault inspect <vault-path>` — get vault metadata (file count, folder count, size)
   - Read files directly from the vault path using standard file tools
   - `obsidian search <vault-path> "query"` — search within a vault
   - Create/edit files in the vault as needed

4. **Before tagging content:** Use the CLI to read all available tags and check if existing ones fit the need. Only create new tags if you're unable to find the appropriate one, and follow the way the other tags are written.

**Personal Vault Structure:**
- Location: `/home/openclaw/Obsidian/Personal`
- 298 files across 56 folders
- Key sections: Home, Property (Campolide & Maia), Hobbies, Clippings, Dashboard

**Default behavior:** If Miguel doesn't specify a vault, use Personal. No asking — just use it.

---

## Hardware

- Running on a **Linux server** (x86_64, user openclaw, host vader)

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## MCP Tools (Docker MCP Gateway)

All MCP needs go through Docker MCP gateway — single source of truth.

**MCP servers:** `home-assistant`, `tp-link-omada`, `mcp-atlassian-miguelms`, `mcp-atlassian-teg`

**I run inside OpenClaw** — always use mcporter to call MCP tools.

```bash
mcporter call <server>.<tool> ...
```

Config: `config/mcporter.json` (stdio servers use `uvx`, HTTP servers use `baseUrl`).

## Web Search

Use the native `web_search` tool — powered by Brave API. No mcporter needed.
- Supports queries, date filters, freshness, language, and country filters
- Use `web_fetch` to retrieve full page content from a URL

## TP-Link Omada (mcporter MCP)

- MCP server name: `tp-link-omada`
- Use for anything about Miguel's **home network**: clients, MAC addresses, IP addresses, signal strength, APs, switches, VLANs, SSIDs, port forwarding, firewall, etc.
- Start with `tp-link-omada.listSites` to get the siteId (`685ac718840b7e743bcc0096` = Maia Home), then use `listClients`, `listDevices`, `getClient`, etc.

## Home Assistant (mcporter MCP)

- MCP server name: `home-assistant`
- Use this server for anything about the **house**, **car**, or smart-home state/control (lights, climate, locks, media, sensors, automations, etc.).
- Prefer starting with `home-assistant.GetLiveContext` when the request depends on current state, then act (e.g., `HassTurnOn`, `HassLightSet`, `HassClimateSetTemperature`).

## TTS (ElevenLabs — Native)

- Engine: **ElevenLabs** via OpenClaw native TTS (no scripts, no exec needed)
- Voice: **Darth Oxley** (`G3zrXA9moYrFCgwBAvxJ`) — Deep and Frightening
- Model: `eleven_turbo_v2_5` (default)

To send a voice message, emit this directive in your reply:
```
[[tts:voiceId=G3zrXA9moYrFCgwBAvxJ]]
```
OpenClaw renders the audio and delivers it automatically to the channel.
No file handling, no message tool calls, no scripts required.
⚠️ Only emit this directive when the user **explicitly asks** for a voice or audio reply. Do not include it in normal text replies.

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Google Drive — AI Generated Images
- Folder: **AI Generated Images** (owned by darth@miguel.ms, shared with joao@miguel.ms as writer)
- Folder ID: `1dXOTBjXtluD2bQem84hGjfRGJk2_Bbqj`
- Upload: `gog drive upload /path/to/image.jpg --account darth@miguel.ms --parent 1dXOTBjXtluD2bQem84hGjfRGJk2_Bbqj`
- URL: https://drive.google.com/drive/folders/1dXOTBjXtluD2bQem84hGjfRGJk2_Bbqj

## Email Signature

- Always append the HTML signature when sending emails via `gog gmail send`
- Signature file: `/home/openclaw/.openclaw/workspace/email-signature.html`
- Usage: `--body-html "<p>Body here.</p>$(cat /home/openclaw/.openclaw/workspace/email-signature.html)"`
- Or for plain text bodies, switch to HTML and prepend the text in a `<p>` block

## Technitium DNS API

- Base URL: `https://dns.miguel.ms`
- API Token: stored in `secrets/technitium.env` (read with `source secrets/technitium.env`)
- Docs: `<host>/api/`

## SSH Hosts

- pve-01.servers.miguel.ms
- pve-02.servers.miguel.ms

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
