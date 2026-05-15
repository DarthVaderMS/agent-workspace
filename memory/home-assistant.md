# Home Assistant

Seed notes for Home Assistant entity and sensor references.

# Home Assistant — Sensor & Entity Reference

## Access

- URL: `https://home.miguel.ms`
- MCP server: `home-assistant` (via mcporter — 22 tools)
- API: `https://home.miguel.ms/api/` — token in vader's mcporter config
- Always prefer `mcporter call home-assistant.<tool>` over raw API calls

---

## Garage

| Sensor | Entity ID | Notes |
|--------|-----------|-------|
| Car in garage box | `sensor.car_in_garage_box` | Returns car name, e.g. "Mercedes A200" |
| Garage box light | `light.garage_box_light` | on/off |
| Garage box power | `sensor.garage_box_power` | Watts (combined motor + light) |
| Garage box energy | `sensor.garage_box_energy` | kWh total |
| Garage thermometer (cold) | `binary_sensor.garage_thermometer_cold` | on = cold |
| Garage thermometer (hot) | `binary_sensor.garage_thermometer_hot` | on = hot |
| Garage box switches online | `binary_sensor.garage_box_switches` | connectivity |

---

## Cars / Vehicles

| Sensor | Entity ID | Notes |
|--------|-----------|-------|
| Car in garage | `sensor.car_in_garage_box` | Which car is currently in the garage box |
| Mercedes A200 (BT-73-BO) tracker | `device_tracker.a200_bt_73_bo_device_tracker` | GPS location, `home`/`not_home` |
| Mercedes A200 car sensor | `sensor.a200_bt_73_bo_car` | VIN W1K3F8HB2SJ502785, last command, status |

---

## People / Presence

| Sensor | Entity ID | Notes |
|--------|-----------|-------|
| Miguel iPhone 15 Pro Max | `device_tracker.miguel_iphone_15_pro_max` | GPS presence |
| Pietra iPhone 13 Pro Max | `device_tracker.pietra_iphone_13_pro_max` | GPS presence |
| Stella's iPhone 17 Pro Max | `device_tracker.stella_s_iphone_17_pro_max` | GPS presence |

---

## House State

| Sensor | Entity ID | Notes |
|--------|-----------|-------|
| Lights on in house | `sensor.house_lights_on` | Count of lights currently on |

---

## Notes

- Use `sensor.car_in_garage_box` as the **primary** entity for "what car is in the garage" queries
- Mercedes A200 integration is via Mercedes Me — last command state visible on sensor attributes
