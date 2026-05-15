# Caddy Reverse Proxy

Last updated: 2026-03-03

- Host: caddy.servers.miguel.ms (LXC 10020 on pve-01), IP: 10.3.10.20
- Version: Caddy v2.11.1
- No Docker — runs directly on the LXC
- Wildcard TLS: `*.miguel.ms` via Cloudflare DNS challenge
- Config: `/etc/caddy/Caddyfile` + `/etc/caddy/sites/miguel.ms/*.caddy`
- Cloudflare trusted proxies configured for real client IP

## Route Map

| Subdomain | Backend | Auth | Notes |
|-----------|---------|------|-------|
| auth.miguel.ms | 10.3.10.15:9090 | — | Vouch auth endpoint |
| chat.miguel.ms | 10.3.10.61:8080 | — | Chat service |
| dns.miguel.ms | 10.3.10.16:443 | — | Technitium DNS (TLS skip verify) |
| docker.miguel.ms | → komo.miguel.ms | — | Redirect to Komodo |
| downloads.miguel.ms | 10.3.10.12:7443 | — | Synology Download Station (TLS) |
| files.miguel.ms | 10.3.10.12:7001 | — | Synology File Station (TLS) |
| garage-gateway.miguel.ms | 10.4.10.1:443 | — | Garage gateway (TLS) |
| home.miguel.ms | 10.3.10.14:443 | — | Home Assistant (TLS) |
| ical.miguel.ms | /Sonarr → 10.3.10.53:80, /Radarr → 10.3.10.52:80 | — | iCal feeds |
| komo.miguel.ms | 10.3.10.30:9120 | — | Komodo |
| n8n.miguel.ms | 10.3.10.43:5678 | — | n8n automation |
| nas.miguel.ms | 10.3.10.12:60443 | — | Synology NAS (TLS) |
| net.miguel.ms | 10.3.10.35:80 | — | Net service |
| nginx.miguel.ms | 10.3.10.13:81 | — | Nginx Proxy Manager UI |
| noco.miguel.ms | 10.3.10.64:8080 | — | NocoDB |
| omada.miguel.ms | 10.3.10.9:8043 | — | TP-Link Omada primary (TLS) |
| omada-bkp.miguel.ms | 10.3.10.10:8043 | — | TP-Link Omada backup (TLS) |
| omada.miguel.ms/mcp | 10.3.10.48:3000 | — | Omada MCP endpoint |
| omada.miguel.ms/sse | 10.3.10.48:3000 | — | Omada SSE endpoint |
| openclaw.miguel.ms | darth-vader-mac.devices.miguel.ms:18789 | — | OpenClaw gateway |
| overseerr.miguel.ms | 10.3.10.59:80 | — | Overseerr |
| photos.miguel.ms | 10.3.10.12:5443 | — | Synology Photos (TLS) |
| plex.miguel.ms | 10.3.10.50:32400 | — | Plex (TLS) |
| prowlarr.miguel.ms | 10.3.10.54:80 | Vouch | Prowlarr |
| puml.miguel.ms | 10.3.10.36:8080 | Vouch | PlantUML |
| pve-01.miguel.ms / pve.miguel.ms | 10.3.10.21:8006 | — | Proxmox PVE-01 (TLS) |
| pve-02.miguel.ms | 10.3.10.22:8006 | — | Proxmox PVE-02 (TLS) |
| qdrant.miguel.ms | 10.3.10.38:6333 | Vouch | Qdrant vector DB |
| radarr.miguel.ms | 10.3.10.52:80 | Vouch | Radarr |
| sonarr.miguel.ms | 10.3.10.53:80 | Vouch | Sonarr |
| sso.miguel.ms | 10.3.10.12:8564 | — | SSO (Synology, TLS) |
| tautulli.miguel.ms | 10.3.10.57:8181 | — | Tautulli |
| torrent.miguel.ms | 10.3.10.51:80 | Vouch | qBittorrent |
| ~~up.miguel.ms~~ | ~~10.3.10.37:80~~ | — | DECOMMISSIONED 2026-03-03 — caddy config deleted, DNS removed |
| wh.miguel.ms | 10.3.10.14:443 | — | Webhook → Home Assistant (EDP energy) |
| wireguard.miguel.ms | 10.3.10.19:10086 | — | WireGuard UI |

## Auth: Vouch SSO
- Vouch proxy at: 10.3.10.15:9090 (auth.miguel.ms)
- Protected services: prowlarr, puml, qdrant, radarr, sonarr, torrent

## Decommissioned Routes
- **up.miguel.ms** → uptime-kuma at 10.3.10.37 — service deleted, Caddy config still present, should be removed
