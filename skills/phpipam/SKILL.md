---
name: phpipam
description: Manage phpIPAM (IP Address Management) via its REST API. Use when asked about IP addresses, subnets, VLANs, VRFs, network sections, or devices in the home network IPAM system. Covers listing/searching IPs and subnets, allocating addresses, managing VLANs, and querying network inventory.
metadata:
  {
    "openclaw":
      {
        "homepage": "https://phpipam.net/api-documentation/",
        "requires": { "env": ["PHPIPAM_URL", "PHPIPAM_APP_ID", "PHPIPAM_TOKEN"] },
        "primaryEnv": "PHPIPAM_TOKEN",
      },
  }
---

# phpIPAM Skill

## Connection

Set these environment variables before calling phpIPAM:

```bash
export PHPIPAM_URL="https://phpipam.example.com"
export PHPIPAM_APP_ID="my_app"
export PHPIPAM_TOKEN="token"
```

`PHPIPAM_TOKEN` is the primary secret. Send it as `phpipam-token: $PHPIPAM_TOKEN` or `token: $PHPIPAM_TOKEN` on every request. Prefer `phpipam-token` in new examples because the official auth reference names it first, while `token` remains supported.

```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/sections/"
```

## Response Format

JSON with `success` (bool), `code` (HTTP status), `data` (payload), `message` (on error).

## Controllers

| Controller | Base Path | Purpose |
|------------|-----------|---------|
| sections | /sections/ | Top-level groupings of subnets |
| subnets | /subnets/ | Subnet management |
| folders | /folders/ | Alias for folder-style subnet objects |
| addresses | /addresses/ | IP address management |
| vlan | /vlan/ | VLAN management |
| l2domains | /l2domains/ | VLAN domain management |
| vrf | /vrf/ | VRF management |
| devices | /devices/ | Device inventory |
| tools | /tools/{subcontroller}/ | Tags, locations, racks, NAT, etc. |
| prefix | /prefix/{customer_type}/... | Automatic subnet/address provisioning |
| search | /search/{string}/ | Global search |

## Common Operations

### List all sections
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/sections/"
```

### List subnets in a section
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/sections/{id}/subnets/"
```

### Search for an IP
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/addresses/search/{ip}/"
```

### Search by hostname
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/addresses/search_hostname/{hostname}/"
```

### Get first free IP in a subnet
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/subnets/{id}/first_free/"
```

### Add an address
```bash
curl -s -X POST -H "phpipam-token: $PHPIPAM_TOKEN" -H "Content-Type: application/json" \
  -d '{"subnetId":1,"ip":"10.3.10.50","hostname":"myhost","description":"My host"}' \
  "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/addresses/"
```

### Search subnet by CIDR
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/subnets/cidr/10.3.10.0%2F24/"
```

### List all VLANs
```bash
curl -s -H "phpipam-token: $PHPIPAM_TOKEN" "$PHPIPAM_URL/api/$PHPIPAM_APP_ID/vlan/"
```

## Notes

- Canonical API docs: https://phpipam.net/api-documentation/
- Current official API reference page reports phpIPAM version 1.7.4: https://phpipam.net/api/api_reference/
- Local API reference summary: see `references/api.md`
- Subnet CIDR in URLs must be URL-encoded: `/` → `%2F`
