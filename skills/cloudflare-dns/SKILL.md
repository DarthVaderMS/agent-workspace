---
name: cloudflare-dns
description: Manage Cloudflare DNS zones and records via the Cloudflare REST API. Use when asked to list zones, list/search DNS records, create/update/delete DNS records, or check DNS settings on Cloudflare. Triggers on requests like "add a DNS record", "list my Cloudflare zones", "delete the CNAME for X", "update the A record for Y", "show all TXT records", etc.
metadata:
  {
    "openclaw":
      {
        "homepage": "https://developers.cloudflare.com/api/",
        "requires": { "env": ["CLOUDFLARE_API_TOKEN"] },
        "primaryEnv": "CLOUDFLARE_API_TOKEN",
      },
  }
---

# Cloudflare DNS

Manage DNS via the Cloudflare API (`https://api.cloudflare.com/client/v4`).

## Auth

Set these environment variables before calling Cloudflare:

```bash
export CLOUDFLARE_API_TOKEN="<token>"
# Optional: set only when you want to filter to one Cloudflare account.
export CLOUDFLARE_ACCOUNT_ID="<account_id>"
```

`CLOUDFLARE_API_TOKEN` is the primary secret and must be sent as `Authorization: Bearer $CLOUDFLARE_API_TOKEN`.
`CLOUDFLARE_ACCOUNT_ID` is optional; leave it unset when managing zones across multiple Cloudflare accounts.

Token permissions:
- Read-only workflows: `Zone Read` and `DNS Read`
- Mutating workflows: `Zone Read` and `DNS Write`
- Prefer a token scoped only to the needed account/zones.

## Common Workflows

### List accounts

Use this first when the token can access multiple Cloudflare accounts and you need the right account ID.

```bash
curl -s "https://api.cloudflare.com/client/v4/accounts?per_page=50" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {id, name, type}'
```

### List zones

```bash
curl -s "https://api.cloudflare.com/client/v4/zones?per_page=50" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {id, name, status}'
```

Filter to a single account only when needed:
```bash
curl -s "https://api.cloudflare.com/client/v4/zones?account.id=$CLOUDFLARE_ACCOUNT_ID&per_page=50" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {id, name, status}'
```

### List DNS records for a zone

```bash
ZONE_ID=<zone_id>
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?per_page=100" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {id, type, name, content, ttl, proxied}'
```

Filter by type: append `&type=A`, `&type=CNAME`, `&type=TXT`, etc.
Filter by name: append `&name.exact=sub.example.com`

### Create a DNS record

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "sub.example.com",
    "content": "1.2.3.4",
    "ttl": 1,
    "proxied": false
  }' | jq '.result | {id, type, name, content}'
```

`ttl: 1` = automatic. Proxied records are effectively automatic TTL.

### Update (patch) a DNS record

```bash
RECORD_ID=<record_id>
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "5.6.7.8"}' | jq '.result | {id, type, name, content}'
```

Use `PATCH` for record edits. Use `PUT` only when intentionally overwriting the full DNS record object.

### Delete a DNS record

```bash
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result'
```

### Find a record by name (to get its ID)

```bash
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name.exact=sub.example.com" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {id, type, content}'
```

## API References

- Zones: https://developers.cloudflare.com/api/resources/zones/
- DNS records: https://developers.cloudflare.com/api/resources/dns/subresources/records/
- DNS record type guide: https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/
- Field examples per record type: see `references/record-types.md`.

## Record Types

Supported by the current API docs: `A`, `AAAA`, `CAA`, `CERT`, `CNAME`, `DNSKEY`, `DS`, `HTTPS`, `LOC`, `MX`, `NAPTR`, `NS`, `OPENPGPKEY`, `PTR`, `SMIMEA`, `SRV`, `SSHFP`, `SVCB`, `TLSA`, `TXT`, `URI`

Key constraints:
- A/AAAA and CNAME cannot coexist on the same name
- NS records cannot coexist with any other type on the same name
- MX requires `priority` field
- SRV requires `data` object (not `content`)

## Error Handling

Check `success` field in response. Errors appear in `errors[]` array with `code` and `message`.

Common codes:
- `81053` – Record already exists
- `81057` – Cannot have A/AAAA and CNAME on same name
- `7003/7000` – Zone not found / invalid token
