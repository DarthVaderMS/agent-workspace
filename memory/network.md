# Network Memory — Maia Home

## Overview

Two locations: **Maia Home** (main) and **Garage** (underground, separate internet, WireGuard-linked).

## ISP & WAN

- **ISP:** Vodafone Portugal — does NOT provide a public IP directly to the network
- **Topology:** Vodafone router → TP-Link gateway (DMZ'd), creating a double-NAT at `192.168.1.0/30`
- `192.168.1.0/30` is the link between the Vodafone CPE and the TP-Link Omada gateway

## Home Network Stack (Maia — 10.3.x.x)

- **Gateway/Router:** TP-Link Omada gateway at `10.3.10.1`
- **Network management:** Full Omada stack — accessible via `tp-link-omada` MCP
- **WireGuard:** Handled by the Omada gateway directly (not the wireguard LXC — that's for user VPN access via WGDashboard)

### VLANs

| VLAN ID | Name | Number | Purpose |
|---------|------|--------|---------|
| Home | Home VLAN | 10 | Default untagged — main LAN |
| IoT | IoT VLAN | 30 | IoT devices, isolated |
| Guest | Guest VLAN | 231 | Wi-Fi guest network |

### Subnets

| Subnet | Description | VLAN | Notes |
|--------|-------------|------|-------|
| 10.3.10.0/23 | Home Subnet | 10 | Parent |
| 10.3.10.0/24 | Static IPs | 10 | Servers, infra |
| 10.3.11.0/24 | Dynamic IPs | 10 | DHCP pool |
| 10.3.30.0/23 | IoT Subnet | 30 | Parent |
| 10.3.30.0/24 | IoT Static IPs | 30 | Fixed IoT |
| 10.3.31.0/24 | IoT Dynamic IPs | 30 | DHCP pool |
| 10.3.40.0/26 | WireGuard VPN | — | User VPN via WGDashboard LXC |
| 10.3.231.0/26 | Guest Subnet | 231 | Wi-Fi guests |
| 192.168.1.0/30 | Internet Routing | — | Vodafone CPE ↔ TP-Link gateway |

### DNS Servers (Home)

| IP | Role |
|----|------|
| 10.3.10.1 | TP-Link Omada gateway |
| 10.3.10.11 | ns1.servers.miguel.ms — Technitium (primary DNS) |
| 10.3.10.12 | Synology NAS — secondary DNS, mirrors Technitium zones (access TBD) |

## Garage Network (10.4.x.x)

- **Location:** Underground garage — separate physical site
- **Internet:** Own internet connection (GSM/mobile)
- **Router:** Teltonika RUT200 (`https://garage-gateway.network.miguel.ms`) (API access configured)
- **Link to home:** WireGuard tunnel via TP-Link Omada gateway (not the wireguard LXC)

### Subnets

| Subnet | Description | VLAN | Notes |
|--------|-------------|------|-------|
| 10.4.0.0/16 | Garage parent | — | |
| 10.4.10.0/23 | Garage LAN | 10 | |
| 10.4.10.0/24 | Static IPs | 10 | |
| 10.4.11.0/24 | Dynamic IPs | 10 | DHCP pool |
| 10.4.30.0/23 | Garage IoT | 30 | |
| 10.4.30.0/24 | Garage IoT Static | 30 | |
| 10.4.31.0/24 | Garage IoT Dynamic | 30 | DHCP pool |

## Public DNS — Cloudflare

- **Zones:** `miguel.ms` and `marquessilva.net`
- **Zone IDs:**
  - `miguel.ms` → `ea75b308ac4030a2e449b1eb148cf220`
  - `marquessilva.net` → `abebc79df943ec45d1d36b9caf5e0ba1`
- **API Token:** `secrets/cloudflare.env`
- **Skill:** `skills/cloudflare-dns`
- **Split-horizon:** Technitium = internal, Cloudflare = public

### ⚠️ Standing Rule — miguel.ms Subdomains

**Whenever Miguel asks to create a subdomain in `miguel.ms`**, always ask:
> *"Should this also be added as a DNS record in Cloudflare?"*

## Pending Access

- Synology NAS (10.3.10.12) — secondary DNS
- Teltonika RUT200 — garage router (`garage-gateway.network.miguel.ms`)

# Network Memory — Maia Home

## Overview

Two locations: **Maia Home** (main) and **Garage** (underground, separate internet, WireGuard-linked).

## ISP & WAN

- **ISP:** Vodafone Portugal — does NOT provide a public IP directly to the network
- **Topology:** Vodafone router → TP-Link gateway (DMZ'd), creating a double-NAT at `192.168.1.0/30`
- `192.168.1.0/30` is the link between the Vodafone CPE and the TP-Link Omada gateway

## Home Network Stack (Maia — 10.3.x.x)

- **Gateway/Router:** TP-Link Omada gateway at `10.3.10.1`
- **Network management:** Full Omada stack — accessible via `tp-link-omada` MCP
- **WireGuard:** Handled by the Omada gateway directly (not the wireguard LXC — that's for user VPN access via WGDashboard)

### VLANs

| VLAN ID | Name | Number | Purpose |
|---------|------|--------|---------|
| Home | Home VLAN | 10 | Default untagged — main LAN |
| IoT | IoT VLAN | 30 | IoT devices, isolated |
| Guest | Guest VLAN | 231 | Wi-Fi guest network |

### Subnets

| Subnet | Description | VLAN | Notes |
|--------|-------------|------|-------|
| 10.3.10.0/23 | Home Subnet | 10 | Parent |
| 10.3.10.0/24 | Static IPs | 10 | Servers, infra |
| 10.3.11.0/24 | Dynamic IPs | 10 | DHCP pool |
| 10.3.30.0/23 | IoT Subnet | 30 | Parent |
| 10.3.30.0/24 | IoT Static IPs | 30 | Fixed IoT |
| 10.3.31.0/24 | IoT Dynamic IPs | 30 | DHCP pool |
| 10.3.40.0/26 | WireGuard VPN | — | User VPN via WGDashboard LXC |
| 10.3.231.0/26 | Guest Subnet | 231 | Wi-Fi guests |
| 192.168.1.0/30 | Internet Routing | — | Vodafone CPE ↔ TP-Link gateway |

### DNS Servers (Home)

| IP | Role |
|----|------|
| 10.3.10.1 | TP-Link Omada gateway |
| 10.3.10.11 | ns1.servers.miguel.ms — Technitium (primary DNS) |
| 10.3.10.12 | Synology NAS — secondary DNS, mirrors Technitium zones (access TBD) |

## Garage Network (10.4.x.x)

- **Location:** Underground garage — separate physical site
- **Internet:** Own internet connection (GSM/mobile)
- **Router:** Teltonika RUT200 (`https://garage-gateway.network.miguel.ms`) (API access configured)
- **Link to home:** WireGuard tunnel via TP-Link Omada gateway (not the wireguard LXC)

### Subnets

| Subnet | Description | VLAN | Notes |
|--------|-------------|------|-------|
| 10.4.0.0/16 | Garage parent | — | |
| 10.4.10.0/23 | Garage LAN | 10 | |
| 10.4.10.0/24 | Static IPs | 10 | |
| 10.4.11.0/24 | Dynamic IPs | 10 | DHCP pool |
| 10.4.30.0/23 | Garage IoT | 30 | |
| 10.4.30.0/24 | Garage IoT Static | 30 | |
| 10.4.31.0/24 | Garage IoT Dynamic | 30 | DHCP pool |

## Public DNS — Cloudflare

- **Zones:** `miguel.ms` and `marquessilva.net`
- **Zone IDs:**
  - `miguel.ms` → `ea75b308ac4030a2e449b1eb148cf220`
  - `marquessilva.net` → `abebc79df943ec45d1d36b9caf5e0ba1`
- **API Token:** stored in `~/.openclaw/workspace/secrets/cloudflare.env` (this workspace)
- **Split-horizon:** Technitium handles internal DNS (`10.3.x.x`), Cloudflare handles public DNS

### ⚠️ Standing Rule — miguel.ms Subdomains

**Whenever Miguel asks to create a subdomain in `miguel.ms`**, always ask:
> *"Should this also be added as a DNS record in Cloudflare?"*

If yes, add via API:
```bash
source ~/.openclaw/workspace/secrets/cloudflare.env
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/ea75b308ac4030a2e449b1eb148cf220/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"A","name":"sub.miguel.ms","content":"<public_ip>","ttl":1,"proxied":false}'
```

## Pending Access

- Synology NAS (10.3.10.12) — secondary DNS
- Teltonika RUT200 — garage router (`garage-gateway.network.miguel.ms`)

## Recent Internal DNS / Proxy Records

- `vader.agents.miguel.ms` -> `10.3.10.67` in Technitium `agents.miguel.ms`.
- `vader.miguel.ms` -> CNAME `http-proxy.services.miguel.ms` in Technitium, served by Caddy on `caddy.servers.miguel.ms` / `10.3.10.20`.
- `velcra-gh-runner.servers.miguel.ms` -> `10.3.10.65` in Technitium `servers.miguel.ms`.
