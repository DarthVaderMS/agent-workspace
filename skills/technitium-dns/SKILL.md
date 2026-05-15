---
name: technitium-dns
description: Manage Miguel's home Technitium DNS server via its HTTP API. Use when asked to manage DNS zones, add/edit/delete DNS records, query DNS, flush cache, view logs, or inspect DNS settings on the home network (miguel.ms). Covers zone management, record CRUD, cache flushing, DNS client queries, and server settings.
metadata:
  {
    "openclaw":
      {
        "homepage": "https://technitium.com/dns/",
        "requires": { "env": ["TECHNITIUM_URL", "TECHNITIUM_TOKEN"] },
        "primaryEnv": "TECHNITIUM_TOKEN",
      },
  }
---

# Technitium DNS Skill

## Connection

- **Base URL:** set `TECHNITIUM_URL`, for example `https://dns.miguel.ms`
- **Token:** set `TECHNITIUM_TOKEN`
- Pass token as `Authorization: Bearer $TECHNITIUM_TOKEN`
- Query string/form `token=` is still supported by Technitium for backward compatibility, but prefer the bearer header.
- Use `curl -sk` (skip TLS verification — internal cert)

## Request Format

All calls accept GET or POST. POST requires `Content-Type: application/x-www-form-urlencoded`.

```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/<endpoint>?param=value"
```

## Response Format

Always JSON with a `status` field:
- `ok` — success
- `error` — failed; check `errorMessage`
- `invalid-token` — token expired or wrong

## Key API Categories

| Category | Base Path | Notes |
|----------|-----------|-------|
| Zones | `/api/zones/...` | List, create, delete, enable/disable zones |
| Records | `/api/zones/records/...` | Add, get, update, delete DNS records |
| Cache | `/api/cache/...` | List, flush cache entries |
| DNS Client | `/api/dnsClient/...` | Resolve queries against the server |
| Settings | `/api/settings/...` | Get/set server configuration |
| Dashboard | `/api/dashboard/...` | Stats and top lists |
| Logs | `/api/logs/...` | Query server logs |

## Common Operations

### List all zones
```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/zones/list"
```

### Get records for a zone
```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/zones/records/get?zone=miguel.ms&domain=miguel.ms"
```

### Add a record
```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/zones/records/add?zone=miguel.ms&domain=test.miguel.ms&type=A&ttl=300&ipAddress=10.3.10.50"
```

### Delete a record
```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/zones/records/delete?zone=miguel.ms&domain=test.miguel.ms&type=A"
```

### Flush cache
```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/cache/flush"
```

### Resolve a name (DNS client)
```bash
curl -sk -H "Authorization: Bearer $TECHNITIUM_TOKEN" \
  "$TECHNITIUM_URL/api/dnsClient/resolve?server=this-server&domain=example.miguel.ms&type=A"
```

## Notes

- Current token is **read-only** — can view zones/records/cache/logs but cannot modify. Ask Miguel to grant write permissions if changes are needed.
- The home network uses miguel.ms with split-horizon DNS — internal zones override public Cloudflare entries.
- Canonical API reference: https://github.com/TechnitiumSoftware/DnsServer/blob/master/APIDOCS.md
- Local API reference mirror: see `references/api.md` (load when you need specific endpoint params or record types not covered above).
