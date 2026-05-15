# Services Memory

Seed notes for Komodo stacks and running services: server, ports, state, deployment ID, and health.

## Omada Controller

- Primary controller: `omada-lxc-controller` on `10.3.10.9` (pve-01), running `Omada Controller v6.2.10.17 Build 20260428102045` after 2026-05-11 upgrade.
- Listener ports observed healthy: `8043`, `8088`, `8843`, `29811-29814`.

## Komodo

- Public URL: `https://komo.miguel.ms`.
- Core container: `komodo-core-1` on `komodo.servers.miguel.ms`.
- Backend DB: MongoDB on `mongodb.servers.miguel.ms:27017`, LXC `10036` on `pve-01`.
- Current DB version: MongoDB `8.3.1` after 2026-05-12 recovery.
- Komodo recovered after MongoDB returned: public URL returned HTTP 200 and Komodo API `ListServers` returned 6 servers.

## Vader OpenClaw Route

- Public URL: `https://vader.miguel.ms`.
- Reverse proxy: `caddy.servers.miguel.ms` / `10.3.10.20`.
- Upstream: `vader.agents.miguel.ms:18789` / `10.3.10.67`.
- Auth: Vouch/Synology for normal paths, `/hooks` bypasses auth.
- Headers forwarded for OpenClaw trusted-proxy auth: `X-Forwarded-User`, `X-Forwarded-Proto`, `X-Forwarded-Host`; Caddy maps `X-Forwarded-User` from `X-Vouch-User`.
- OpenClaw scopes header: `X-OpenClaw-Scopes: operator.admin,operator.read,operator.write,operator.approvals,operator.pairing,operator.talk.secrets`.
