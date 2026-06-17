# beacon_challenge_api

A very small local API for the WebUI beacon challenge.

It uses only the Python standard library, so it can run locally without Docker,
virtual environments, or third-party packages.

## Run locally

```bash
python3 app.py
```

The API starts on:

```text
http://127.0.0.1:8000
```

You can choose another host or port with environment variables:

```bash
HOST=0.0.0.0 PORT=5000 python3 app.py
```

## Endpoint

```text
GET /data
```

Example:

```bash
curl http://127.0.0.1:8000/data
```

The endpoint returns one random simulated item from a 40-device in-memory fleet
of surveillance equipment, including fixed CCTV cameras, PTZ cameras, thermal
cameras, ANPR cameras, UAVs, tethered UAVs, motion detectors, perimeter radar,
acoustic arrays, RF detectors, tracking beacons, and access control sensors.
Each item keeps state while the API process is running, so the same devices will
show up repeatedly with slightly different location, battery, health,
detection, and type-specific readings. Battery level declines every time a
device is returned, then resets to `100.0` when it reaches zero.

Example response:

```json
{
  "ID": "PTZ-CAMERA-0002",
  "type": "ptz_camera",
  "lat": 53.151831,
  "long": -1.803941,
  "battery_level": 77.4,
  "active": true,
  "data": {
    "device_health": {
      "firmware": "3.8.12",
      "uptime_seconds": 581204,
      "temperature_c": 42.3,
      "storage_used_percent": 63.8,
      "last_contact_seconds_ago": 3
    },
    "coverage": {
      "bearing_deg": 188,
      "range_m": 821.4,
      "sector": "east_fence"
    },
    "detections": {
      "objects_tracked": 7,
      "person_count": 3,
      "vehicle_count": 1,
      "unknown_count": 0,
      "confidence_percent": 94.2,
      "last_event": {
        "event_id": "evt-391847",
        "age_seconds": 18,
        "classification": "person",
        "priority": "medium"
      }
    },
    "video": {
      "resolution": "4k",
      "fps": 30,
      "bitrate_kbps": 10620,
      "autotracking": true
    },
    "ptz": {
      "pan_deg": 217,
      "tilt_deg": 12,
      "zoom_level": 8.4,
      "preset": "perimeter"
    }
  },
  "signal": "active"
}
```

Rarely, a device will report as inactive and return no type-specific data:

```json
{
  "ID": "THERMAL-CAMERA-0013",
  "type": "thermal_camera",
  "lat": 51.507351,
  "long": -0.127758,
  "battery_level": 42.1,
  "active": false,
  "data": null,
  "signal": "inactive"
}
```
