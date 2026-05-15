# Teltonika RUT200 API Endpoints Reference

Miguel unit last tested: firmware 7.21.1 | API v1.13.1
Current public RUT200 firmware page checked 2026-05-13:
- Stable firmware: RUT2M_R_00.07.22.1, released 2026-04-13
- Latest firmware: RUT2M_R_00.07.23.1, released 2026-05-05

Docs:
- Current RUT200 API entrypoint: https://developers.teltonika-networks.com/reference/rut200/
- Last-tested unit docs: https://developers.teltonika-networks.com/reference/rut200/7.21.1/v1.13.1/
- Latest public docs path checked 2026-05-13: https://developers.teltonika-networks.com/reference/rut200/7.23.1/

Auth header: `Authorization: Bearer <token>`
RutOS 7.19+ also added HTTP Basic Authentication support for API use. Prefer bearer-session login unless a specific device/version is known to require Basic auth.

## Authentication (works on Miguel's unit)
- `POST /api/login` — `{"username":"...","password":"..."}` → returns token
- `POST /api/logout` — end session
- `GET /api/session/status` — check + reset session timer

## API v1 endpoints
Base path: `/api/v1/...` (availability depends on firmware/modules; some devices may return `Endpoint not implemented`).

## System
- `GET /system` — system info (hostname, uptime, firmware, model)
- `POST /system/reboot` — reboot device
- `GET /firmware` — firmware version info
- `POST /firmware` — upgrade firmware

## Network & Interfaces
- `GET /interfaces` — all interfaces + IP/status
- `GET /interfaces/{name}` — specific interface
- `PUT /interfaces/{name}` — configure interface
- `GET /network` — network overview
- `GET /ip/routes` — routing table
- `GET /ip/rules` — policy routing rules
- `GET /ip/neighbors` — ARP/neighbor table
- `GET /routing/tables` — routing tables

## Internet / WAN
- `GET /internet/connection` — WAN connection status
- `GET /failover` — failover/load balancing config
- `PUT /failover` — configure failover

## Mobile / GSM
- `GET /modems` — modem list + status (signal, operator, technology)
- `GET /sim/cards` — SIM card details (ICCID, IMSI, operator, signal)
- `GET /data/usage` — mobile data consumption stats
- `GET /data/limit` — data limit config
- `PUT /data/limit` — set data limit
- `GET /operator/lists` — operator lists
- `GET /apn/database` — APN database
- `GET /modem/control` — modem control settings

## WireGuard
- `GET /wireguard` — WireGuard instances + peer status
- `POST /wireguard` — create WireGuard instance
- `PUT /wireguard/{id}` — update instance
- `DELETE /wireguard/{id}` — delete instance

## DHCP
- `GET /dhcp/servers` — DHCP server config
- `PUT /dhcp/servers` — configure DHCP server
- `GET /dhcp/leases` — active leases (IP, MAC, hostname, expiry)

## Firewall
- `GET /firewall` — all firewall rules
- `POST /firewall` — add rule
- `PUT /firewall/{id}` — update rule
- `DELETE /firewall/{id}` — delete rule
- `GET /firewall/dmz` — DMZ config
- `GET /attack/prevention` — DoS/attack prevention settings

## DNS
- `GET /dns` — DNS config (servers, search domains)
- `PUT /dns` — update DNS config
- `GET /ddns` — Dynamic DNS config/status
- `PUT /ddns` — configure DDNS

## Wireless (Wi-Fi)
- `GET /wireless` — Wi-Fi interfaces + clients
- `PUT /wireless` — configure Wi-Fi
- `GET /wifi/scanner` — scan for nearby APs

## VPN
- `GET /openvpn` — OpenVPN instances
- `GET /ipsec` — IPsec tunnels
- `GET /l2tp` — L2TP config
- `GET /pptp` — PPTP config
- `GET /gre` — GRE tunnels
- `GET /vrrp` — VRRP config

## Diagnostics & Troubleshooting
- `POST /troubleshoot/diagnostics` — run ping/traceroute: `{"type":"ping","host":"...","count":4}`
- `GET /troubleshoot` — troubleshoot tools
- `GET /topology` — network topology
- `POST /speedtest` — run speed test

## Logging & Events
- `GET /logging` — system logs
- `GET /events/log` — event log
- `GET /traffic/logging` — traffic logs

## SMS (RUT200 has GSM)
- `GET /messages` — SMS inbox
- `POST /messages` — send SMS
- `GET /sms/utilities` — SMS utilities config
- `GET /sms/gateway` — SMS gateway config

## Services
- `GET /services` — running services
- `GET /snmp` — SNMP config
- `GET /mqtt` — MQTT broker config
- `GET /ntp` — NTP / date-time config
- `GET /upnp` — UPnP config

## Access & Security
- `GET /users` — user accounts
- `GET /access/control` — remote access config
- `GET /password/policy` — password policy
- `GET /certificates` — TLS certificates

## Backup & Config
- `GET /backup` — download config backup
- `POST /backup` — restore backup
- `GET /profiles` — config profiles
