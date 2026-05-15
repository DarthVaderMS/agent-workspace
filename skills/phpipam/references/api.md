# phpIPAM API Reference

Source: https://phpipam.net/api-documentation/
Official API reference page reports current phpIPAM version: 1.7.4.

## Request Methods

| Method | Description |
|--------|-------------|
| OPTIONS | Returns all supported controllers and methods |
| GET | Reads object(s) |
| POST | Creates new object |
| PUT/PATCH | Updates object |
| DELETE | Deletes object |

## Request Format

```
<METHOD> /api/<APP_ID>/<controller>/ HTTP/1.1
Content-Type: application/json
phpipam-token: <TOKEN>
Host: <HOST>
```

## Response Format

Always JSON with `success` (bool), `code` (HTTP), `message` (on error), `data` (on success).

## Authentication

**Dynamic (user/pass → token):**
```bash
curl -X POST -H "Authorization: Basic $(echo -n 'user:pass' | base64)" \
  https://<HOST>/api/<APP_ID>/user/
# Returns: {"token":"...","expires":"..."}
```

**Static token** (defined per app in phpIPAM UI — recommended for automation):
```bash
curl -H "phpipam-token: <TOKEN>" https://<HOST>/api/<APP_ID>/sections/
```

Token must be included as `phpipam-token` or `token` header on every request. Prefer `phpipam-token` for new examples; `token` remains supported.

## Controllers

### Sections — `/api/{app}/sections/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /sections/ | All sections |
| GET | /sections/{id}/ | Specific section |
| GET | /sections/{id}/subnets/ | All subnets in section |
| GET | /sections/{name}/ | Section by name |
| POST | /sections/ | Create section |
| PATCH | /sections/ | Update section |
| DELETE | /sections/ | Delete section (+ all subnets/addresses) |

### Subnets — `/api/{app}/subnets/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /subnets/ | All subnets |
| GET | /subnets/{id}/ | Specific subnet |
| GET | /subnets/{id}/usage/ | Subnet usage stats |
| GET | /subnets/{id}/slaves/ | Immediate child subnets |
| GET | /subnets/{id}/slaves_recursive/ | All child subnets |
| GET | /subnets/{id}/addresses/ | All addresses in subnet |
| GET | /subnets/{id}/addresses/{ip}/ | Specific IP in subnet |
| GET | /subnets/{id}/first_free/ | First available IP |
| GET | /subnets/{id}/first_subnet/{mask}/ | First available child subnet |
| GET | /subnets/cidr/{subnet}/ | Search by CIDR |
| GET | /subnets/search/{subnet}/ | Search by CIDR (alias) |
| POST | /subnets/ | Create subnet |
| POST | /subnets/{id}/first_subnet/{mask}/ | Create first available child subnet |
| PATCH | /subnets/ | Update subnet |
| PATCH | /subnets/{id}/resize/ | Resize subnet |
| PATCH | /subnets/{id}/split/ | Split subnet |
| DELETE | /subnets/{id}/ | Delete subnet |
| DELETE | /subnets/{id}/truncate/ | Remove all addresses from subnet |

Key params: `subnet` (IP), `mask` (int), `sectionId`, `vlanId`, `vrfId`, `masterSubnetId`, `description`

### Folders — `/api/{app}/folders/`

Folder is an alias for the subnets controller. Folder objects are represented as subnet records with `isFolder=1`.

### Addresses — `/api/{app}/addresses/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /addresses/{id}/ | Specific address |
| GET | /addresses/all/ | All addresses |
| GET | /addresses/{ip}/{subnetId}/ | Address by IP in subnet |
| GET | /addresses/search/{ip}/ | Search by IP |
| GET | /addresses/search_hostname/{hostname}/ | Search by hostname |
| GET | /addresses/search_mac/{mac}/ | Search by MAC |
| GET | /addresses/first_free/{subnetId}/ | First free address |
| GET | /addresses/tags/ | All tags |
| POST | /addresses/ | Create address |
| POST | /addresses/first_free/{subnetId}/ | Create at first free slot |
| PATCH | /addresses/{id}/ | Update address |
| DELETE | /addresses/{id}/ | Delete address |
| DELETE | /addresses/{ip}/{subnetId}/ | Delete by IP in subnet |

Key params: `subnetId`, `ip`, `hostname`, `mac`, `description`, `is_gateway`, `tag`, `deviceId`, `note`

### VLANs — `/api/{app}/vlan/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /vlan/ | All VLANs |
| GET | /vlan/{id}/ | Specific VLAN |
| GET | /vlan/{id}/subnets/ | Subnets in VLAN |
| POST | /vlan/ | Create VLAN |
| PATCH | /vlan/ | Update VLAN |
| DELETE | /vlan/ | Delete VLAN |

Key params: `name`, `number` (VLAN ID), `domainId`, `description`

### L2 Domains — `/api/{app}/l2domains/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /l2domains/ | All L2 domains |
| GET | /l2domains/all/ | All L2 domains (alias) |
| GET | /l2domains/{id}/ | Specific L2 domain |
| GET | /l2domains/{id}/vlans/ | VLANs within L2 domain |
| GET | /l2domains/custom_fields/ | L2 domain custom fields |
| POST | /l2domains/ | Create L2 domain |
| PATCH | /l2domains/ | Update L2 domain |
| DELETE | /l2domains/ | Delete L2 domain |

### VRFs — `/api/{app}/vrf/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /vrf/ | All VRFs |
| GET | /vrf/{id}/ | Specific VRF |
| GET | /vrf/{id}/subnets/ | Subnets in VRF |
| POST | /vrf/ | Create VRF |
| PATCH | /vrf/ | Update VRF |
| DELETE | /vrf/ | Delete VRF |

### Devices — `/api/{app}/devices/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | /devices/ | All devices |
| GET | /devices/{id}/ | Specific device |
| GET | /devices/{id}/addresses/ | Addresses for device |
| GET | /devices/search/{string}/ | Search devices |
| POST | /devices/ | Create device |
| PATCH | /devices/ | Update device |
| DELETE | /devices/ | Delete device |

Key params: `hostname`, `ip_addr`, `description`, `sections`

### Tools — `/api/{app}/tools/{subcontroller}/`

Subcontrollers: `tags`, `devices`, `device_types`, `vlans`, `vrfs`, `nameservers`, `scanagents`, `locations`, `nat`, `racks`

### Search — `/api/{app}/search/{string}/`

Searches across addresses, subnets, VLANs, VRFs.

### Prefix — `/api/{app}/prefix/{customer_type}/{address_type}/{mask}/`

Auto-provisioning controller — returns/creates first available subnet or address from pools marked with a custom field.

## Global Parameters

Add to any request:
- `filter_by=<field>` + `filter_value=<value>` — filter results
- `filter_match=full|partial|regex`
- `links=false` — suppress HATEOAS links in response
