---
name: teltonika-rut200
description: Manage Miguel's Teltonika RUT200 garage router via its REST API. Use when asked about the garage router, garage network, GSM/mobile internet, WireGuard tunnel to garage, modem/SIM status, garage DHCP leases, garage firewall, or any configuration/status on the RUT200. Device is at the underground garage location, connects to home network via WireGuard through the Omada gateway.
metadata:
  {
    "openclaw":
      {
        "homepage": "https://developers.teltonika-networks.com/reference/rut200/",
        "requires": { "env": ["RUT200_URL", "RUT200_USERNAME", "RUT200_PASSWORD"] },
        "primaryEnv": "RUT200_PASSWORD",
      },
  }
---

# Teltonika RUT200 Skill

## Device Context

- **Device:** Teltonika RUT200 (GSM router) — garage location
- **Connection to home:** WireGuard tunnel via Omada gateway (not the wireguard LXC)
- **Network:** 10.4.0.0/16 (garage), LAN 10.4.10.0/23, IoT 10.4.30.0/23
- **Miguel unit last tested:** firmware 7.21.1 | API v1.13.1
- **Current public RUT200 firmware page, checked 2026-05-13:** stable 00.07.22.1, latest 00.07.23.1

## Connection

Set these environment variables before calling the router:

```bash
export RUT200_URL="https://router.example"
export RUT200_USERNAME="admin"
export RUT200_PASSWORD="password"
```

`RUT200_PASSWORD` is the primary secret. Do not print it, commit it, or include it in logs.

## Authentication

The API requires a session token obtained via login. Tokens expire — check before use.

```bash
# Login — get token
TOKEN=$(curl -sk --compressed -X POST "$RUT200_URL/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$RUT200_USERNAME\",\"password\":\"$RUT200_PASSWORD\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

# Check session
curl -sk --compressed -H "Authorization: Bearer $TOKEN" "$RUT200_URL/api/session/status"

# Logout
curl -sk --compressed -X POST -H "Authorization: Bearer $TOKEN" "$RUT200_URL/api/logout"
```

RutOS 7.19+ added HTTP Basic Authentication support for API use, but bearer-session login remains the safest default because it works on Miguel's last-tested unit and keeps examples compatible with the existing endpoint reference.

## Request Format

```bash
curl -sk --compressed -H "Authorization: Bearer $TOKEN" "$RUT200_URL/api/v1/<endpoint>"
# POST/PUT: add -X POST -H "Content-Type: application/json" -d '{...}'
```

Note: on Miguel's current unit, `/api/login`, `/api/session/status` work; many `/api/v1/*` endpoints may return `Endpoint not implemented` depending on enabled modules/firmware.

Response format: `{"success": true/false, "data": {...}}`

## Key Endpoints

| Category | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| **System** | /system | GET | System info (uptime, firmware, hostname) |
| **Interfaces** | /interfaces | GET | All network interfaces + status |
| **Internet** | /internet/connection | GET | WAN/mobile connection status |
| **Modems** | /modems | GET | GSM modem list + status |
| **SIM cards** | /sim/cards | GET | SIM info (operator, signal, ICCID) |
| **Data usage** | /data/usage | GET | Mobile data usage stats |
| **WireGuard** | /wireguard | GET | WireGuard peers + status |
| **WireGuard** | /wireguard | PUT | Update WireGuard config |
| **DHCP** | /dhcp/servers | GET | DHCP server config |
| **DHCP leases** | /dhcp/leases | GET | Active DHCP leases |
| **Firewall** | /firewall | GET | Firewall rules |
| **DNS** | /dns | GET | DNS configuration |
| **Diagnostics** | /troubleshoot/diagnostics | POST | Ping/traceroute from router |
| **Events Log** | /events/log | GET | System event log |
| **Logging** | /logging | GET | System logs |
| **Reboot** | /system/reboot | POST | Reboot device |
| **Firmware** | /firmware | GET | Firmware info |
| **DDNS** | /ddns | GET | Dynamic DNS config/status |
| **Failover** | /failover | GET | WAN failover config |

## Common Operations

### Check modem/SIM signal
```bash
curl -sk -H "Authorization: Bearer $TOKEN" "$RUT200_URL/api/v1/modems"
```

### Check WireGuard tunnel status
```bash
curl -sk -H "Authorization: Bearer $TOKEN" "$RUT200_URL/api/v1/wireguard"
```

### List DHCP leases (who's connected)
```bash
curl -sk -H "Authorization: Bearer $TOKEN" "$RUT200_URL/api/v1/dhcp/leases"
```

### Run ping from router
```bash
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"ping","host":"10.3.10.1","count":4}' \
  "$RUT200_URL/api/v1/troubleshoot/diagnostics"
```

## Notes

- Current RUT200 firmware downloads: https://wiki.teltonika-networks.com/view/RUT200_Firmware_Downloads
- Current RUT200 Web API docs entrypoint: https://developers.teltonika-networks.com/reference/rut200/
- Last-tested API reference for Miguel's unit: https://developers.teltonika-networks.com/reference/rut200/7.21.1/v1.13.1/authentication
- Latest public API docs path checked 2026-05-13: https://developers.teltonika-networks.com/reference/rut200/7.23.1/authentication
- Full endpoint list: see `references/endpoints.md`
