# Infrastructure Memory

Last updated: 2026-05-15

## Assistant Handling

- Miguel removed the old blanket rule that infrastructure questions require delegation.
- Vader handles infrastructure requests directly when tools, access, and permission make it safe.
- External or destructive infrastructure changes still require explicit approval when they change configuration or service state.

## SSH Access Policy

- Default SSH user for infrastructure hosts is usually `root`.
- If `root` is not allowed, Miguel will say so or the verified host entry should record the exception.
- Keep `/home/openclaw/.ssh/config` updated as access is verified.
- Current verified exception: `tegclaw` uses user `openclaw` with `/home/openclaw/.ssh/id_ed25519_vader`.

## Proxmox GPU Notes

- 2026-05-14: `pve-02.servers.miguel.ms` runs kernel `7.0.2-2-pve` with NVIDIA driver `580.126.09` on RTX 3080 Ti. Installer exists at `/root/NVIDIA-Linux-x86_64-580.126.09.run`.
- 2026-05-14: `pve-03.servers.miguel.ms` runs kernel `7.0.2-2-pve` with GeForce 940MX (`10de:134d`). Attempted same `580.126.09` installer. Open kernel module builds but does not support this pre-GSP GPU; proprietary kernel module fails against Proxmox kernel headers due GPL-only `__vma_start_write` path. Cleaned failed NVIDIA install and restored `nouveau`; installer remains in `/root`.
- 2026-05-14: `pve-03` lid close behavior configured. `/etc/systemd/logind.conf.d/99-ignore-lid.conf` makes logind ignore lid-close for suspend/shutdown. `acpid` is installed/enabled with `/etc/acpi/events/lid-screen-blank` and `/etc/acpi/actions/lid-screen-blank.sh` to run `setterm --blank force` on close and `setterm --blank poke` on open. No `/sys/class/backlight` controls were exposed.

## Proxmox HA Notes

- 2026-05-15: Cluster `home` has three nodes: `pve-01` (10.3.10.21), `pve-03` (10.3.10.23), and `pve-02` (10.3.10.22). HA services `pve-ha-lrm` and `pve-ha-crm` were enabled and started on all three after Miguel explicitly approved the config change.
- HA-managed resources after final verification: CTs `10009`, `10011`, `10013`, `10019`, `10020`, `10030`, `10031`, `10032`, `10033`, `10034`, `10036`, `10039`, `10064`, `10065`, `10067`, and VM `10014`; all were `started`, quorum OK, fencing armed, master `pve-02`.
- Final placement after settling: pve-01 runs `10011`, `10020`, `10031`, `10033`, `10036`, `10039`; pve-02 runs `10034`, `10064`, `10065`, `10067`; pve-03 runs `10009`, `10013`, `10019`, `10030`, `10032`.
- HA affinity rules at final verification: `ha-rule-41bed9ac-0cdc` ("Default") targets pve-01-local CTs `10020,10031,10033,10036,10039`; `ha-rule-95059e86-0a27` ("Inverted Dafault") targets `10009,10019`; `ha-rule-pve03-default` targets `10030`; `ha-rule-7e82e276-fe8b` targets NVIDIA/GPU-related CTs `10034,10064,10067`; `ha-rule-a214e2d7-748d` targets Home Assistant VM `10014`.
- Gotchas encountered: local-lvm/local-hdd storage and snapshots caused aborted migrations for some pve-01 services. `ct:10020` hit HA `error` because HA tried to start it while a disk move still held a `disk` lock; recovered by temporarily setting HA state disabled, starting the CT, then setting state back to started. When changing HA rules with `ha-manager rules set`, quote comma-separated `--nodes` values or they may not apply as intended.

## TEGClaw

- Hostname: `tegclaw.servers.miguel.ms`
- Internal IP: `10.3.10.66`
- SSH alias: `ssh tegclaw`
- SSH config: user `openclaw`, identity `/home/openclaw/.ssh/id_ed25519_vader`, `IdentitiesOnly yes`
- Host keys are stored in `/home/openclaw/.ssh/known_hosts`
- Verified 2026-05-13: read-only SSH succeeds and remote reports hostname `tegclaw`, user `openclaw`

## Komodo
- URL: https://komo.miguel.ms
- Version: Komodo Core v2
- Skill env vars: `KOMODO_URL`, `KOMODO_API_KEY`, `KOMODO_API_SECRET`
- All stacks sourced from GitHub repo: MiguelTVMS/komodo-settings (branch: main)

---

## Servers (7)

| Name | Address | Region | Notes |
|------|---------|--------|-------|
| Apps | docker-app.servers.miguel.ms:8120 | — | General apps server |
| Docker GPU | docker-gpu.servers.miguel.ms:8120 | PVE-02 | RTX 3080 Ti, GPU workloads |
| Komodo | komodo.servers.miguel.ms:8120 | — | Komodo itself |
| Lab | docker-lab.servers.miguel.ms:8120 | — | Lab/testing |
| NAS | nas.servers.miguel.ms:8120 | — | NAS |
| Net | docker-net.servers.miguel.ms:8120 | — | Networking / proxy |
| Openclaw | openclaw.servers.miguel.ms:8120 | — | OpenClaw host |

All servers: state OK. Komodo has been updated to Core v2; verify individual Periphery agent versions live before relying on older 1.x notes.

---

## Stacks (16)

| Name | Server | State | Services |
|------|--------|-------|---------|
| ddns | Net | running | cloudflare-ddns ×2 (miguel.ms + rentrack.store) |
| hear | Docker GPU | running | whisper ASR (GPU) |
| media-management | Apps | running | prowlarr, radarr, sonarr, qbittorrent, flaresolverr |
| minecraft | Apps | running | bedrock-survival (Minecraft Bedrock) |
| n8n | Docker GPU | running | n8n-server + supporting services |
| nocodb | Apps | running | nocodb |
| ollama | Docker GPU | running | ollama (GPU) |
| omada-mcp | Docker GPU | running | jmtvms/tplink-omada-mcp |
| open-webui | Docker GPU | running | open-webui |
| phpipam | Apps | running | phpipam-web + phpipam-mariadb + phpipam-cron |
| plex | Apps | running | plex server + overseerr + tautulli |
| qdrant | Docker GPU | running | qdrant (GPU, nvidia) |
| redis | Docker GPU | **DOWN** (decommissioned) | redis:8-alpine — stack kept, volumes already gone |
| speak | Openclaw | running | piper TTS |
| uptime-kuma | Apps | **DECOMMISSIONED** | Deleted from Komodo 2026-03-03. IP: 10.3.10.37, hostname: uptime-kuma.servers.miguel.ms, network: local_ipvlan, data at /opt/uptime-kuma/data |
| vouch | Net | running | vouch-proxy |

### Notes:
- **redis** → Docker GPU, kept as shell (decommissioned, no volumes)
- **uptime-kuma** → decommissioned 2026-03-03, DNS/IP reserved: 10.3.10.37 / uptime-kuma.servers.miguel.ms

---

## Repos (1)
- **komodo-settings** → github.com/MiguelTVMS/komodo-settings (main) — single source of truth for all stack configs

---

## Procedures (3)
- **Backup Core Database** — scheduled daily
- **Global Auto Update** — scheduled (checks for image updates)
- **Global Clean Up** — scheduled (2-stage, prune)

---

## Builders (1)
- **Local** — Server type builder

---

## Questions for Miguel
- redis is DOWN on Docker GPU — intentional or needs restart?
- uptime-kuma is STOPPED (exit code 1) — intentional or broken?
- Several stacks have outdated deployed_hash vs latest_hash (ddns, hear, media-management, omada-mcp, plex, qdrant, redis) — pending sync from komodo-settings repo

# Infrastructure Memory

Last updated: 2026-05-13

## Komodo
- URL: https://komo.miguel.ms
- Version: 1.19.5
- Credentials: ~/workspace/secrets/komodo.env
- All stacks sourced from GitHub repo: MiguelTVMS/komodo-settings (branch: main)
- Backend DB: `mongodb.servers.miguel.ms` / LXC `10036` on `pve-01`, MongoDB `8.3.1` after 2026-05-12 recovery.

---

## Servers (7)

| Name | Address | Region | Notes |
|------|---------|--------|-------|
| Apps | docker-app.servers.miguel.ms:8120 | — | General apps server |
| Docker GPU | docker-gpu.servers.miguel.ms:8120 | PVE-02 | RTX 3080 Ti, GPU workloads |
| Komodo | komodo.servers.miguel.ms:8120 | — | Komodo itself |
| Lab | docker-lab.servers.miguel.ms:8120 | — | Lab/testing |
| NAS | nas.servers.miguel.ms:8120 | — | NAS |
| Net | docker-net.servers.miguel.ms:8120 | — | Networking / proxy |
| Openclaw | openclaw.servers.miguel.ms:8120 | — | OpenClaw host |

All servers: state OK, Periphery 1.19.5.

---

## Stacks (16)

| Name | Server | State | Services |
|------|--------|-------|---------|
| ddns | Net | running | cloudflare-ddns ×2 (miguel.ms + rentrack.store) |
| hear | Docker GPU | running | whisper ASR (GPU) |
| media-management | Apps | running | prowlarr, radarr, sonarr, qbittorrent, flaresolverr |
| minecraft | Apps | running | bedrock-survival (Minecraft Bedrock) |
| n8n | Docker GPU | running | n8n-server + supporting services |
| nocodb | Apps | running | nocodb |
| ollama | Docker GPU | running | ollama (GPU) |
| omada-mcp | Docker GPU | running | jmtvms/tplink-omada-mcp |
| open-webui | Docker GPU | running | open-webui |
| phpipam | Apps | running | phpipam-web + phpipam-mariadb + phpipam-cron |
| plex | Apps | running | plex server + overseerr + tautulli |
| qdrant | Docker GPU | running | qdrant (GPU, nvidia) |
| redis | Docker GPU | **DOWN** (decommissioned) | redis:8-alpine — stack kept, volumes already gone |
| speak | Openclaw | running | piper TTS |
| uptime-kuma | Apps | **DECOMMISSIONED** | Deleted from Komodo 2026-03-03. IP: 10.3.10.37, hostname: uptime-kuma.servers.miguel.ms, network: local_ipvlan, data at /opt/uptime-kuma/data |
| vouch | Net | running | vouch-proxy |

### Notes:
- **redis** → Docker GPU, kept as shell (decommissioned, no volumes)
- **uptime-kuma** → decommissioned 2026-03-03, DNS/IP reserved: 10.3.10.37 / uptime-kuma.servers.miguel.ms

---

## Repos (1)
- **komodo-settings** → github.com/MiguelTVMS/komodo-settings (main) — single source of truth for all stack configs

---

## Procedures (3)
- **Backup Core Database** — scheduled daily
- **Global Auto Update** — scheduled (checks for image updates)
- **Global Clean Up** — scheduled (2-stage, prune)

---

## Builders (1)
- **Local** — Server type builder

---

## Questions for Miguel
- redis is DOWN on Docker GPU — intentional or needs restart?
- uptime-kuma is STOPPED (exit code 1) — intentional or broken?
- Several stacks have outdated deployed_hash vs latest_hash (ddns, hear, media-management, omada-mcp, plex, qdrant, redis) — pending sync from komodo-settings repo

---

## TEGClaw LXC (added 2026-03-15)

| Field | Value |
|-------|-------|
| LXC ID | 10064 (pve-02) |
| Hostname | tegclaw.servers.miguel.ms |
| IP | 10.3.10.66 (Home Static VLAN) |
| RAM | 4 GB |
| OS | Debian 13 Trixie |
| Node.js | v24.14.0 (system-wide, nodesource) |
| OpenClaw | 2026.3.13, installed as `openclaw` user, npm global prefix `~/.npm-global` |
| Assistant | zeus (anthropic:default key, claude-sonnet-4-6 primary, no fallback) |
| Workspace | /home/openclaw/.openclaw/workspace-zeus |
| Gateway port | 18789, bind=lan, mDNS=off |
| Channels | None — web UI only (https://tegclaw.miguel.ms) |
| Vouch | Disabled — OpenClaw token auth only |
| Gateway token | in ~/.openclaw/.env as OPENCLAW_GATEWAY_TOKEN |
| Health monitor | channelHealthCheckMinutes=35000 (effectively disabled) |
| GPU | RTX 3080 Ti passthrough (/dev/nvidia* visible), NVIDIA driver 580.126.09 installed (userspace only, --no-kernel-module) |
| Homebrew | 5.1.0 installed in /home/linuxbrew/.linuxbrew, PATH set for openclaw user |
| SSH access | Miguel's RSA + Vader's ed25519 keys in /home/openclaw/.ssh/authorized_keys |
| Linger | Enabled for openclaw user (survives logout) |
| Public URL | https://tegclaw.miguel.ms (Caddy → tegclaw.servers.miguel.ms:18789, no Vouch) |

### Snapshots (pve-02, LXC 10064)
| Snapshot | Description |
|----------|-------------|
| pre-openclaw-install | Clean Debian 13, no Node/OC |
| pre-openclaw-config | Node 24 + OC 2026.3.8 installed |
| zeus-ready | OC 2026.3.13, agent zeus configured, web UI ready |
| pre-nvidia-install | Before NVIDIA driver install |
| pre-homebrew | NVIDIA 580.126.09 installed, before Homebrew |
| pre-qmd | Homebrew 5.1.0 + NVIDIA, before QMD |
| pre-lossless-claw | Before LCM/lossless-claw install |

---

## Velcra GitHub Runner LXC (added 2026-05-03)

| Field | Value |
|-------|-------|
| LXC ID | 10065 (pve-02) |
| Hostname | velcra-gh-runner.servers.miguel.ms |
| IP | 10.3.10.65 (Home Static VLAN) |
| OS | Ubuntu 24.04.4 LTS |
| Resources | 16 cores, 16 GB RAM, 4 GB swap, 200 GB rootfs on local-lvm |
| Purpose | Base host for future GitHub Actions runner, runner not installed/registered yet |
| Network | vmbr0, gateway 10.3.10.1, DNS A record in Technitium servers.miguel.ms |
| phpIPAM | Address ID 1619, subnet 29 |
| Features | unprivileged LXC, nesting=1, keyctl=1, onboot=1 |
| Base tools | git, curl, jq, unzip, zip, sudo, gnupg, build-essential, python3, python3-pip, uidmap, fuse-overlayfs, openssh-server, htop, btop, nvme-cli, pciutils |
| Snapshot | clean-ubuntu-base-20260503 |
| Notes | Proxmox local-lvm is thin-provisioned and overcommitted by nominal volume size; actual used was ~36.7% after creation. |

---

## Vader Agents OpenClaw LXC (added 2026-05-13)

| Field | Value |
|-------|-------|
| LXC ID | 10067 (pve-02) |
| Hostname | vader.agents.miguel.ms |
| IP | 10.3.10.67 (Home Static VLAN) |
| OS | Ubuntu 24.04.4 LTS |
| Resources | 12 cores, 16 GB RAM, 4 GB swap, 120 GB rootfs on local-lvm |
| Purpose | GPU-enabled base host for a future OpenClaw install; OpenClaw not installed yet |
| Network | vmbr0, gateway 10.3.10.1, DNS A record in Technitium agents.miguel.ms |
| Public URL | https://vader.miguel.ms (Caddy -> vader.agents.miguel.ms:18789, Vouch auth; `/hooks` bypasses auth) |
| phpIPAM | Address ID 1620, subnet 29 |
| Features | unprivileged LXC, nesting=1, keyctl=1, onboot=1 |
| GPU | RTX 3080 Ti passthrough (/dev/nvidia* visible), NVIDIA driver/userspace 580.126.09 installed with `--no-kernel-module` |
| User | `openclaw` with Miguel/Vader SSH keys, sudo, video/render groups, passwordless sudo |
| Base tools | git, curl, jq, unzip, zip, sudo, gnupg, build-essential, python3, python3-pip, openssh-server, htop, btop, pciutils, kmod |
| Snapshot | clean-ubuntu-gpu-base-20260513 |
| Notes | Proxmox local-lvm is thin-provisioned and overcommitted by nominal volume size; actual used was ~39.1% before creation. |

### Vader Caddy / Trusted Proxy Notes (added 2026-05-13)
- Public route: `https://vader.miguel.ms` on `caddy.servers.miguel.ms`.
- Upstream: `http://vader.agents.miguel.ms:18789`.
- Auth: Vouch/Synology via `https://auth.miguel.ms/login`; `/hooks` bypasses Vouch.
- Caddy forwards `X-Vouch-User`, maps it to `X-Forwarded-User`, and forwards `X-Forwarded-Proto` + `X-Forwarded-Host`.
- OpenClaw trusted-proxy values for this route: proxy IP `10.3.10.20`, `userHeader: "x-forwarded-user"`, required headers `x-forwarded-proto,x-forwarded-host`, allowed user `miguel`.
- Caddy also injects `X-OpenClaw-Scopes: operator.admin,operator.read,operator.write,operator.approvals,operator.pairing,operator.talk.secrets`.
- Connectivity verified: public `/hooks` and direct upstream `/hooks` both returned HTTP 200 after OpenClaw was listening; response was the OpenClaw UI HTML, so functional webhook tests need a deeper webhook path/token.

---

## Omada Controllers (Network Management)

| Component | Status | Details |
|-----------|--------|---------|
| **Primary** | ✅ Operational | omada-lxc-controller (10.3.10.9, pve-01) running v6.2.10.17 Build 20260428102045 |
| **Backup** | ❌ Decommissioned | omada-bkp-controller (was LXC 10010, pve-02) — deleted 2026-04-14 due to v6.2.10.11 HSB initialization timeout |
| **Cluster mode** | Standalone | Primary running alone; HSB disabled |
| **Network traffic** | Handled by primary | Network fully operational |
| **High availability** | Broken | Single point of failure. To restore: downgrade backup to v6.2.0.17 (working) or wait for v6.2.10.x patch |

**Recent history:**
- 2026-04-13: Upgraded both controllers from v6.2.0.17 to v6.2.10.11
- 2026-04-14: Backup failed HSB initialization; decommissioned after troubleshooting
- 2026-04-26: Primary upgraded to v6.2.10.15 Build 20260417100356 after snapshot `pre-omada-6-2-10-15-20260426`
- 2026-05-11: Primary upgraded to v6.2.10.17 Build 20260428102045 after snapshot `pre-omada-6-2-10-17-20260511`

---

### Key lessons from tegclaw setup (2026-03-15)
- OpenClaw must run as a dedicated user (not root) with linger enabled — root user services die on session end
- If there's a stale openclaw install on another user, it will call cleanStaleGatewayProcessesSync on startup and SIGTERM the running gateway → kill all stale services first
- `channelHealthCheckMinutes: 99999` overflows 32-bit int (Node sets timer to 1ms) — use ≤35000
- `discovery.mdns.mode: "off"` is a top-level config key (not under `gateway`)
- `gateway.bind: "lan"` is the correct LAN bind mode (not `"0.0.0.0"`, not `bindMode`)
- Device pairing is required per browser profile — token alone is not enough for web UI
- Do NOT add `trustedProxies` unless specifically needed — caused confusion
- Config schema changes fast — always check `/usr/lib/node_modules/openclaw/docs/` on the running version before editing
