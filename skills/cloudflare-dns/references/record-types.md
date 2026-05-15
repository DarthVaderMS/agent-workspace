# Cloudflare DNS Record Types — Field Reference

Base fields present on all record types:
- `type` (string, required) — record type
- `name` (string, required) — complete DNS record name, including the zone name
- `ttl` (number) — seconds; `1` = automatic; range 60–86400 (30+ for Enterprise)
- `proxied` (boolean) — Cloudflare proxy status; only meaningful for proxiable record types
- `comment` (string, optional) — human note on the record
- `tags` (array, optional) — record tags

---

## A / AAAA

```json
{
  "type": "A",
  "name": "sub.example.com",
  "content": "1.2.3.4",
  "ttl": 1,
  "proxied": true
}
```

- `content`: IPv4 (A) or IPv6 (AAAA)
- Can be proxied

---

## CNAME

```json
{
  "type": "CNAME",
  "name": "www.example.com",
  "content": "target.example.com",
  "ttl": 1,
  "proxied": true
}
```

- `content`: target hostname
- Cannot coexist with A/AAAA on the same name

---

## MX

```json
{
  "type": "MX",
  "name": "example.com",
  "content": "mail.example.com",
  "priority": 10,
  "ttl": 3600
}
```

- `priority` (number, required)
- Cannot be proxied

---

## TXT

```json
{
  "type": "TXT",
  "name": "_dmarc.example.com",
  "content": "v=DMARC1; p=none;",
  "ttl": 3600
}
```

- `content`: the text value (quoted strings handled automatically)
- Cannot be proxied

---

## NS

```json
{
  "type": "NS",
  "name": "sub.example.com",
  "content": "ns1.example.com",
  "ttl": 86400
}
```

- Cannot coexist with any other record type on the same name
- Cannot be proxied

---

## SRV

```json
{
  "type": "SRV",
  "name": "_sip._tcp.example.com",
  "data": {
    "priority": 10,
    "weight": 20,
    "port": 5060,
    "target": "sip.example.com"
  },
  "ttl": 3600
}
```

- Uses `data` object instead of `content`
- Cannot be proxied

---

## CAA

```json
{
  "type": "CAA",
  "name": "example.com",
  "data": {
    "flags": 0,
    "tag": "issue",
    "value": "letsencrypt.org"
  },
  "ttl": 3600
}
```

- `tag`: `issue`, `issuewild`, or `iodef`
- Cannot be proxied

---

## PTR

```json
{
  "type": "PTR",
  "name": "4.3.2.1.in-addr.arpa",
  "content": "sub.example.com",
  "ttl": 3600
}
```

---

## DS / DNSKEY

```json
{
  "type": "DS",
  "name": "example.com",
  "data": {
    "key_tag": 12345,
    "algorithm": 13,
    "digest_type": 2,
    "digest": "abcdef1234..."
  },
  "ttl": 3600
}
```

- Used for DNSSEC delegation material.
- Field names and required values depend on whether the record is `DS` or `DNSKEY`; check the live API docs before writing.

---

## SSHFP

```json
{
  "type": "SSHFP",
  "name": "example.com",
  "data": {
    "algorithm": 1,
    "type": 1,
    "fingerprint": "abcdef1234..."
  },
  "ttl": 3600
}
```

---

## TLSA / SMIMEA / OPENPGPKEY

```json
{
  "type": "TLSA",
  "name": "_443._tcp.example.com",
  "data": {
    "usage": 3,
    "selector": 1,
    "matching_type": 1,
    "certificate": "abcdef1234..."
  },
  "ttl": 3600
}
```

- Certificate/key material record schemas vary by type; check the live API docs before writing.

---

## HTTPS / SVCB

```json
{
  "type": "HTTPS",
  "name": "example.com",
  "data": {
    "priority": 1,
    "target": ".",
    "value": "alpn=h2"
  },
  "ttl": 3600
}
```

---

## NAPTR / URI / LOC / CERT

These are supported by Cloudflare's current DNS Records API, but their schemas are more specialized. Check the live API docs before writing:
- API record schema: https://developers.cloudflare.com/api/resources/dns/subresources/records/
- DNS record type guide: https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/

---

## Proxied vs. Non-proxied

Usually proxiable: A, AAAA, CNAME.

Usually DNS-only: CAA, CERT, DNSKEY, DS, LOC, MX, NAPTR, NS, OPENPGPKEY, PTR, SMIMEA, SRV, SSHFP, SVCB, TLSA, TXT, URI.

HTTPS records can be generated automatically by Cloudflare for proxied domains with compatible settings; check the live docs before manually creating or editing HTTPS/SVCB records.
