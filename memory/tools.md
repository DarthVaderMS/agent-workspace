# Tool Quirks & Workarounds

---

## Komodo API

- **Auth:** Use `source /home/openclaw/.openclaw/workspace/secrets/komodo.env` → `$KOMODO_KEY` / `$KOMODO_SECRET`
- The keys in `~/.openclaw/.env` (`KOMODO_VADER_KEY/SECRET`) may be stale — confirmed broken 2026-03-18
- Endpoint pattern: `POST $KOMODO_URL/read/<Action>` or `POST $KOMODO_URL/execute/<Action>`
- `ListStacks` returns an array; if it returns `{"error": "failed to authenticate api key"}` → key is wrong
- Stack destruction: `POST /execute/DestroyStack` with `{"stack": "<name>", "remove_contents": false}`

---

## Omada MCP (`omada-mcp`)

- Server name in mcporter is `omada-mcp` (not `tp-link-omada` — that was the old name, no longer valid)
- Always start with `omada-mcp.listSites` → siteId `685ac718840b7e743bcc0096` (Maia Home)
- `getGatewayWanStatus` requires `gatewayMac` — get it from `listDevices` first
- Traffic/data usage stats: use `omada-mcp.listMostActiveClients` or `listClientsActivity`

---

## Technitium DNS

- Delete A record requires specifying `&ipAddress=<ip>` in addition to `&type=A` — without it the API returns `ok` but does NOT delete the record
- Pattern: `?token=$TOKEN&zone=<zone>&domain=<fqdn>&type=A&ipAddress=<ip>`

---

## Omada Controller dpkg Upgrade

- Interactive installer (whiptail dialog) fails on non-TTY SSH sessions
- Fix: `DEBIAN_FRONTEND=noninteractive dpkg -i <package>.deb`
- Or use: `ssh -tt` with `DEBIAN_FRONTEND=noninteractive`
- The `.deb` package is distributed as a `.deb.zip` — must unzip first
- Download URL pattern (official release): `https://static.tp-link.com/upload/software/YYYY/YYYYMM/YYYYMMDD/<filename>.deb`
- OTA build URL pattern: `https://ota-download.tplinkcloud.com/firmware/<filename>.deb`
- In April 2026, the public release page lagged the requested `6.2.10.15` build; the exact OTA `.deb` was the reliable source for that version.

---

## mcporter call — string type params

- Some tools require string params even when they look like integers (e.g. Confluence `page_id`)
- Shell argument `page_id=1867779` passes as int → validation error
- Fix: use `--args '{"page_id": "1867779", ...}'` with full JSON payload

---

## Confluence Update

- Page ID for Infrastructure page: `1867779` (space: AIM, miguelms.atlassian.net)
- Update via: `mcporter call mcp-atlassian-miguelms.confluence_update_page --args '{"page_id":"1867779", "title":"Infrastructure", "content":"...", ...}'`
- Must use `--args` JSON flag — shell positional args coerce int types incorrectly

---

# memory/tools.md — Dev Tool Quirks & Issues

## mcporter + mcp-atlassian-miguelms Integration (Broken)

**Status**: ❌ Non-functional as of 2026-04-10

### The Problem
`mcp-atlassian-miguelms` MCP server crashes on startup with:
```
ImportError: in `fakeredis.aioredis`, `FakeConnection` renamed to `FakeRedisConnection` in newer fakeredis
```

**Root cause**: Newer `fakeredis` package renamed the class, but the MCP server was built against the old API.

### Cached Artifact
**Location**: `/home/openclaw/.cache/uv/archive-v0/hTemU9_3H8CrCrPiNwdjP/`
**Why it persists**: Archive is cached at the package level, not the MCP server level.
**Attempted fix**: `uv cache clean` does not help (same archive is re-downloaded).
**Proper fix**: Miguel needs to update the docket or pin `fakeredis` version in the MCP server's `pyproject.toml`.

### Workaround (In Use Since 2026-04-10)
**Use Confluence REST API directly** instead of mcporter.
- Requires: `CONFLUENCE_USER` and `CONFLUENCE_TOKEN` env vars
- Endpoint: `https://miguelms.atlassian.net/wiki/api/v2/pages/{page_id}/children`
- Response parsing: Use `children` array, filter by `type: "page"`, extract `id` and title
- Success rate: 100% (no hangs, immediate responses)

**Example call pattern**:
```bash
curl -u "${CONFLUENCE_USER}:${CONFLUENCE_TOKEN}" \
  "https://miguelms.atlassian.net/wiki/api/v2/pages/99026/children"
```

### Impact on Cron Jobs
- **Blog Auto-Publish cron** uses REST API directly as workaround (2026-04-10 onward)
- **Confluence page fetches** bypass mcporter entirely
- **No regression** — REST API is faster and more reliable than mcporter was

### Long-term Fix
Awaiting Miguel to:
1. Pin `fakeredis` version in MCP server, or
2. Update MCP server code to use new class name, or
3. Replace mcporter Confluence integration entirely

# Tool Quirks & Patterns

Operational notes on tool behavior, gotchas, and successful usage patterns.
