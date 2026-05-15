# Decommissioned Resources

---

## 2026-03-18 — open-webui

| Field | Value |
|-------|-------|
| Service | Open WebUI (LLM interface for Ollama) |
| Stack | `open-webui` (Komodo) |
| Server | Docker GPU (`docker-gpu.servers.miguel.ms`) |
| IP | 10.3.10.61 |
| Hostname | `open-webui.servers.miguel.ms` |
| Public URL | `chat.miguel.ms` (Caddy: `/etc/caddy/sites/miguel.ms/chat.caddy`) |
| DNS removed | `open-webui.servers.miguel.ms` A → 10.3.10.61 (Technitium, servers.miguel.ms zone) |
| DNS removed | `chat.miguel.ms` CNAME → http-proxy.services.miguel.ms (Technitium, miguel.ms zone) |
| Caddy removed | `/etc/caddy/sites/miguel.ms/chat.caddy` |
| phpIPAM removed | ID 1596, 10.3.10.61 |
| Cloudflare | No records existed |
| Reason | Requested by Miguel |
| Stack destroyed via | Komodo `DestroyStack` API |
| Backup | None taken — Miguel did not request one |

---

## 2026-04-14 — omada-bkp-controller (LXC 10010)

| Field | Value |
|-------|-------|
| Service | Omada controller (secondary/backup in HSB cluster) |
| LXC | 10010 (pve-02) |
| Hostname | omada-bkp-controller.network.miguel.ms |
| IP | 10.3.10.10 |
| Region | Home Static VLAN (10.3.10.0/24) |
| Reason | v6.2.10.11 HSB secondary initialization timeout — unrecoverable after troubleshooting |
| Issue | Backup controller upgrade to v6.2.10.11 failed. Secondary couldn't initialize replset despite primary being operational. Attempted: HSB state clear, hostname resolution fix, resource check, multiple restarts. All failed. |
| Decision | After 1+ hour of troubleshooting, primary is fully operational and can handle load standalone. Decommission backup to avoid confusion and free resources. |
| LXC deleted | Yes (2026-04-14) |
| IP released | phpIPAM ID 1476, released to pool |
| DNS removed | omada-bkp-controller.network.miguel.ms A record removed from network.miguel.ms zone (Technitium) |
| Primary status | omada-lxc-controller (10.3.10.9) running v6.2.10.11 Build 20260403150649 — fully operational, handling all network traffic |
| Backup available | None — single point of failure. To restore HA: downgrade backup to v6.2.0.17 or wait for v6.2.10.x patch |

---
