#!/usr/bin/env python3
"""A tiny local API for simulated field monitoring equipment."""

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

EQUIPMENT_TYPES = (
    "fixed_cctv_camera",
    "ptz_camera",
    "thermal_camera",
    "anpr_camera",
    "uav",
    "tethered_uav",
    "motion_detector",
    "perimeter_radar",
    "acoustic_array",
    "rf_detector",
    "tracking_beacon",
    "access_control_sensor",
)

ReadingValue = Any


@dataclass
class Equipment:
    id: str
    type: str
    lat: float
    long: float
    battery_level: float
    active: bool = True
    readings: Dict[str, ReadingValue] = field(default_factory=dict)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def build_initial_readings(equipment_type: str) -> Dict[str, ReadingValue]:
    readings: Dict[str, ReadingValue] = {
        "device_health": {
            "firmware": f"{random.randint(1, 4)}.{random.randint(0, 9)}.{random.randint(0, 15)}",
            "uptime_seconds": random.randint(600, 2_500_000),
            "temperature_c": round(random.uniform(18, 58), 1),
            "storage_used_percent": round(random.uniform(12, 89), 1),
            "last_contact_seconds_ago": random.randint(0, 45),
        },
        "coverage": {
            "bearing_deg": random.randint(0, 359),
            "range_m": round(random.uniform(25, 2400), 1),
            "sector": random.choice(("north_gate", "east_fence", "south_yard", "west_road", "central_compound")),
        },
        "detections": {
            "objects_tracked": random.randint(0, 18),
            "person_count": random.randint(0, 9),
            "vehicle_count": random.randint(0, 6),
            "unknown_count": random.randint(0, 4),
            "confidence_percent": round(random.uniform(72, 99), 1),
            "last_event": {
                "event_id": f"evt-{random.randint(100000, 999999)}",
                "age_seconds": random.randint(0, 600),
                "classification": random.choice(("person", "vehicle", "unknown", "wildlife", "no_motion")),
                "priority": random.choice(("low", "medium", "high")),
            },
        },
    }

    if equipment_type == "fixed_cctv_camera":
        readings["video"] = {
            "resolution": random.choice(("1080p", "1440p", "4k")),
            "fps": random.choice((15, 24, 30, 60)),
            "bitrate_kbps": random.randint(1800, 12000),
            "dropped_frames_last_minute": random.randint(0, 16),
            "night_mode": random.choice((True, False)),
        }
        readings["scene"] = {
            "light_level_lux": round(random.uniform(0.2, 1000), 1),
            "occlusion_percent": round(random.uniform(0, 12), 1),
            "motion_regions": random.randint(0, 7),
        }
    elif equipment_type == "ptz_camera":
        readings["video"] = {
            "resolution": random.choice(("1080p", "1440p", "4k")),
            "fps": random.choice((24, 30, 60)),
            "bitrate_kbps": random.randint(2200, 14000),
            "autotracking": random.choice((True, False)),
        }
        readings["ptz"] = {
            "pan_deg": random.randint(0, 359),
            "tilt_deg": random.randint(-35, 60),
            "zoom_level": round(random.uniform(1, 30), 1),
            "preset": random.choice(("gate", "perimeter", "parking", "loading_bay", "patrol")),
        }
    elif equipment_type == "thermal_camera":
        readings["thermal"] = {
            "average_temperature_c": round(random.uniform(8, 38), 1),
            "max_temperature_c": round(random.uniform(28, 82), 1),
            "heat_signatures": random.randint(0, 16),
            "thermal_contrast": random.choice(("low", "medium", "high")),
        }
        readings["image"] = {
            "palette": random.choice(("white_hot", "black_hot", "ironbow")),
            "calibration_age_seconds": random.randint(10, 7200),
            "noise_level": round(random.uniform(0.01, 0.2), 3),
        }
    elif equipment_type == "anpr_camera":
        readings["plates"] = {
            "reads_last_minute": random.randint(0, 18),
            "reads_last_hour": random.randint(20, 900),
            "watchlist_hits": random.randint(0, 3),
            "average_read_confidence_percent": round(random.uniform(78, 99), 1),
            "last_plate": f"{random.choice(('AB', 'YX', 'LD', 'KP', 'MW'))}{random.randint(10, 99)} {random.choice(('CDE', 'FJK', 'LMN', 'RST', 'VWX'))}",
        }
        readings["lane"] = {
            "lane_id": random.randint(1, 6),
            "direction": random.choice(("inbound", "outbound")),
            "average_vehicle_speed_kph": round(random.uniform(8, 70), 1),
        }
    elif equipment_type == "uav":
        readings["flight"] = {
            "altitude_m": round(random.uniform(40, 160), 1),
            "speed_mps": round(random.uniform(0, 22), 1),
            "heading_deg": random.randint(0, 359),
            "gps_accuracy_m": round(random.uniform(0.6, 4.5), 1),
            "return_to_base": random.choice((True, False)),
        }
        readings["mission"] = {
            "waypoint_index": random.randint(1, 18),
            "route_completion_percent": round(random.uniform(0, 100), 1),
            "payload_mode": random.choice(("visual", "thermal", "tracking", "mapping")),
        }
    elif equipment_type == "tethered_uav":
        readings["flight"] = {
            "altitude_m": round(random.uniform(20, 90), 1),
            "heading_deg": random.randint(0, 359),
            "station_keeping_error_m": round(random.uniform(0.1, 6.5), 1),
            "wind_compensation_percent": round(random.uniform(4, 72), 1),
        }
        readings["tether"] = {
            "cable_length_m": round(random.uniform(24, 110), 1),
            "tension_n": round(random.uniform(35, 180), 1),
            "power_draw_w": round(random.uniform(120, 720), 1),
        }
    elif equipment_type == "motion_detector":
        readings["motion"] = {
            "zones_triggered": random.sample(("A", "B", "C", "D", "E"), random.randint(0, 3)),
            "motion_score": round(random.uniform(0, 100), 1),
            "last_motion_seconds_ago": random.randint(0, 7200),
            "sensitivity": random.choice(("low", "medium", "high")),
            "tamper_detected": random.choice((False, False, False, True)),
        }
    elif equipment_type == "perimeter_radar":
        readings["radar"] = {
            "tracks": random.randint(0, 24),
            "fastest_target_kph": round(random.uniform(0, 95), 1),
            "nearest_target_m": round(random.uniform(8, 850), 1),
            "sweep_rate_rpm": random.choice((12, 24, 36, 48)),
            "clutter_percent": round(random.uniform(0, 18), 1),
        }
    elif equipment_type == "acoustic_array":
        readings["audio"] = {
            "sound_level_db": round(random.uniform(28, 96), 1),
            "bearing_to_loudest_source_deg": random.randint(0, 359),
            "detected_events": random.randint(0, 30),
            "classification": random.choice(("speech", "vehicle", "impact", "alarm", "ambient")),
            "snr_db": round(random.uniform(5, 38), 1),
        }
    elif equipment_type == "rf_detector":
        readings["rf"] = {
            "signals_detected": random.randint(0, 18),
            "strongest_frequency_mhz": round(random.uniform(433, 5800), 2),
            "rssi_dbm": random.randint(-104, -32),
            "suspected_protocol": random.choice(("wifi", "lte", "remote_control", "bluetooth", "unknown")),
            "direction_estimate_deg": random.randint(0, 359),
        }
    elif equipment_type == "tracking_beacon":
        readings["beacon"] = {
            "signal_strength_dbm": random.randint(-92, -38),
            "ping_count": random.randint(50, 7000),
            "geofence_state": random.choice(("inside", "edge", "outside")),
            "last_seen_by": random.choice(("tower-a", "tower-b", "mobile-relay-1", "uav-relay-3")),
            "movement_speed_mps": round(random.uniform(0, 18), 1),
        }
    else:
        readings["access_control"] = {
            "door_state": random.choice(("closed", "open", "forced", "held_open")),
            "badge_reads_last_hour": random.randint(0, 260),
            "denied_entries_last_hour": random.randint(0, 18),
            "last_credential_result": random.choice(("granted", "denied", "expired", "unknown")),
            "lock_voltage_v": round(random.uniform(11.2, 13.1), 2),
        }

    return readings


def build_equipment_list(count: int = 40) -> List[Equipment]:
    equipment: List[Equipment] = []

    for index in range(1, count + 1):
        equipment_type = EQUIPMENT_TYPES[(index - 1) % len(EQUIPMENT_TYPES)]
        equipment.append(
            Equipment(
                id=f"{equipment_type.upper().replace('_', '-')}-{index:04d}",
                type=equipment_type,
                lat=round(random.uniform(49.85, 58.65), 6),
                long=round(random.uniform(-7.55, 1.75), 6),
                battery_level=round(random.uniform(25, 100), 1),
                readings=build_initial_readings(equipment_type),
            )
        )

    return equipment


EQUIPMENT = build_equipment_list()


def drift_number(value: Union[float, int], amount: float, low: Optional[float] = None, high: Optional[float] = None) -> float:
    updated = float(value) + random.uniform(-amount, amount)
    if low is not None and high is not None:
        updated = clamp(updated, low, high)
    return updated


def drift_int(value: Union[float, int], amount: int, low: int, high: int) -> int:
    return int(clamp(int(value) + random.randint(-amount, amount), low, high))


def update_common_readings(readings: Dict[str, ReadingValue]) -> None:
    health = readings["device_health"]
    health["uptime_seconds"] = int(health["uptime_seconds"]) + random.randint(1, 20)
    health["temperature_c"] = round(drift_number(health["temperature_c"], 0.4, -10, 85), 1)
    health["storage_used_percent"] = round(drift_number(health["storage_used_percent"], 0.2, 0, 100), 1)
    health["last_contact_seconds_ago"] = random.randint(0, 45)

    coverage = readings["coverage"]
    coverage["bearing_deg"] = int((int(coverage["bearing_deg"]) + random.randint(-4, 4)) % 360)
    coverage["range_m"] = round(drift_number(coverage["range_m"], 12, 5, 4000), 1)

    detections = readings["detections"]
    detections["objects_tracked"] = drift_int(detections["objects_tracked"], 3, 0, 60)
    detections["person_count"] = drift_int(detections["person_count"], 2, 0, 40)
    detections["vehicle_count"] = drift_int(detections["vehicle_count"], 1, 0, 25)
    detections["unknown_count"] = drift_int(detections["unknown_count"], 1, 0, 20)
    detections["confidence_percent"] = round(drift_number(detections["confidence_percent"], 1.8, 35, 100), 1)

    last_event = detections["last_event"]
    last_event["age_seconds"] = int(last_event["age_seconds"]) + random.randint(1, 30)
    if random.random() < 0.16:
        last_event["event_id"] = f"evt-{random.randint(100000, 999999)}"
        last_event["age_seconds"] = 0
        last_event["classification"] = random.choice(("person", "vehicle", "unknown", "wildlife", "no_motion"))
        last_event["priority"] = random.choice(("low", "medium", "high"))


def update_readings(equipment: Equipment) -> Dict[str, ReadingValue]:
    readings = dict(equipment.readings)
    update_common_readings(readings)

    if equipment.type == "fixed_cctv_camera":
        video = readings["video"]
        scene = readings["scene"]
        video["bitrate_kbps"] = drift_int(video["bitrate_kbps"], 450, 500, 20000)
        video["dropped_frames_last_minute"] = drift_int(video["dropped_frames_last_minute"], 3, 0, 120)
        scene["light_level_lux"] = round(drift_number(scene["light_level_lux"], 25, 0, 1200), 1)
        scene["occlusion_percent"] = round(drift_number(scene["occlusion_percent"], 1.2, 0, 100), 1)
        scene["motion_regions"] = drift_int(scene["motion_regions"], 1, 0, 12)
        if random.random() < 0.05:
            video["night_mode"] = not bool(video["night_mode"])
    elif equipment.type == "ptz_camera":
        video = readings["video"]
        ptz = readings["ptz"]
        video["bitrate_kbps"] = drift_int(video["bitrate_kbps"], 500, 500, 22000)
        ptz["pan_deg"] = int((int(ptz["pan_deg"]) + random.randint(-14, 14)) % 360)
        ptz["tilt_deg"] = drift_int(ptz["tilt_deg"], 4, -45, 75)
        ptz["zoom_level"] = round(drift_number(ptz["zoom_level"], 0.9, 1, 36), 1)
        if random.random() < 0.08:
            ptz["preset"] = random.choice(("gate", "perimeter", "parking", "loading_bay", "patrol"))
    elif equipment.type == "thermal_camera":
        thermal = readings["thermal"]
        image = readings["image"]
        thermal["average_temperature_c"] = round(drift_number(thermal["average_temperature_c"], 0.8, -20, 60), 1)
        thermal["max_temperature_c"] = round(drift_number(thermal["max_temperature_c"], 1.6, -10, 120), 1)
        thermal["heat_signatures"] = drift_int(thermal["heat_signatures"], 2, 0, 60)
        image["calibration_age_seconds"] = int(image["calibration_age_seconds"]) + random.randint(1, 30)
        image["noise_level"] = round(drift_number(image["noise_level"], 0.01, 0, 1), 3)
    elif equipment.type == "anpr_camera":
        plates = readings["plates"]
        lane = readings["lane"]
        plates["reads_last_minute"] = drift_int(plates["reads_last_minute"], 4, 0, 80)
        plates["reads_last_hour"] = max(int(plates["reads_last_hour"]) + random.randint(0, 14), 0)
        plates["watchlist_hits"] = drift_int(plates["watchlist_hits"], 1, 0, 20)
        plates["average_read_confidence_percent"] = round(drift_number(plates["average_read_confidence_percent"], 1.3, 20, 100), 1)
        lane["average_vehicle_speed_kph"] = round(drift_number(lane["average_vehicle_speed_kph"], 2.8, 0, 140), 1)
        if random.random() < 0.14:
            plates["last_plate"] = f"{random.choice(('AB', 'YX', 'LD', 'KP', 'MW'))}{random.randint(10, 99)} {random.choice(('CDE', 'FJK', 'LMN', 'RST', 'VWX'))}"
    elif equipment.type == "uav":
        flight = readings["flight"]
        mission = readings["mission"]
        flight["altitude_m"] = round(drift_number(flight["altitude_m"], 5, 0, 220), 1)
        flight["speed_mps"] = round(drift_number(flight["speed_mps"], 1.8, 0, 32), 1)
        flight["heading_deg"] = int((int(flight["heading_deg"]) + random.randint(-12, 12)) % 360)
        flight["gps_accuracy_m"] = round(drift_number(flight["gps_accuracy_m"], 0.25, 0.3, 12), 1)
        mission["route_completion_percent"] = round(clamp(float(mission["route_completion_percent"]) + random.uniform(0, 2.4), 0, 100), 1)
        if random.random() < 0.07:
            mission["waypoint_index"] = int(mission["waypoint_index"]) + 1
    elif equipment.type == "tethered_uav":
        flight = readings["flight"]
        tether = readings["tether"]
        flight["altitude_m"] = round(drift_number(flight["altitude_m"], 1.6, 5, 130), 1)
        flight["heading_deg"] = int((int(flight["heading_deg"]) + random.randint(-8, 8)) % 360)
        flight["station_keeping_error_m"] = round(drift_number(flight["station_keeping_error_m"], 0.5, 0, 20), 1)
        flight["wind_compensation_percent"] = round(drift_number(flight["wind_compensation_percent"], 3, 0, 100), 1)
        tether["tension_n"] = round(drift_number(tether["tension_n"], 4, 10, 260), 1)
        tether["power_draw_w"] = round(drift_number(tether["power_draw_w"], 18, 50, 900), 1)
    elif equipment.type == "motion_detector":
        motion = readings["motion"]
        motion["motion_score"] = round(drift_number(motion["motion_score"], 8, 0, 100), 1)
        motion["last_motion_seconds_ago"] = random.randint(0, 7200)
        if random.random() < 0.2:
            motion["zones_triggered"] = random.sample(("A", "B", "C", "D", "E"), random.randint(0, 3))
        if random.random() < 0.04:
            motion["tamper_detected"] = not bool(motion["tamper_detected"])
    elif equipment.type == "perimeter_radar":
        radar = readings["radar"]
        radar["tracks"] = drift_int(radar["tracks"], 4, 0, 80)
        radar["fastest_target_kph"] = round(drift_number(radar["fastest_target_kph"], 6, 0, 160), 1)
        radar["nearest_target_m"] = round(drift_number(radar["nearest_target_m"], 25, 1, 2000), 1)
        radar["clutter_percent"] = round(drift_number(radar["clutter_percent"], 1.5, 0, 100), 1)
    elif equipment.type == "acoustic_array":
        audio = readings["audio"]
        audio["sound_level_db"] = round(drift_number(audio["sound_level_db"], 2.8, 15, 130), 1)
        audio["bearing_to_loudest_source_deg"] = int((int(audio["bearing_to_loudest_source_deg"]) + random.randint(-9, 9)) % 360)
        audio["detected_events"] = drift_int(audio["detected_events"], 3, 0, 120)
        audio["snr_db"] = round(drift_number(audio["snr_db"], 1.4, 0, 60), 1)
        if random.random() < 0.1:
            audio["classification"] = random.choice(("speech", "vehicle", "impact", "alarm", "ambient"))
    elif equipment.type == "rf_detector":
        rf = readings["rf"]
        rf["signals_detected"] = drift_int(rf["signals_detected"], 3, 0, 80)
        rf["strongest_frequency_mhz"] = round(drift_number(rf["strongest_frequency_mhz"], 12, 100, 6200), 2)
        rf["rssi_dbm"] = drift_int(rf["rssi_dbm"], 3, -120, -20)
        rf["direction_estimate_deg"] = int((int(rf["direction_estimate_deg"]) + random.randint(-10, 10)) % 360)
        if random.random() < 0.08:
            rf["suspected_protocol"] = random.choice(("wifi", "lte", "remote_control", "bluetooth", "unknown"))
    elif equipment.type == "tracking_beacon":
        beacon = readings["beacon"]
        beacon["signal_strength_dbm"] = drift_int(beacon["signal_strength_dbm"], 3, -120, -25)
        beacon["ping_count"] = int(beacon["ping_count"]) + random.randint(1, 8)
        beacon["movement_speed_mps"] = round(drift_number(beacon["movement_speed_mps"], 0.8, 0, 35), 1)
        if random.random() < 0.08:
            beacon["geofence_state"] = random.choice(("inside", "edge", "outside"))
        if random.random() < 0.05:
            beacon["last_seen_by"] = random.choice(("tower-a", "tower-b", "mobile-relay-1", "uav-relay-3"))
    else:
        access = readings["access_control"]
        access["badge_reads_last_hour"] = max(int(access["badge_reads_last_hour"]) + random.randint(0, 4), 0)
        access["denied_entries_last_hour"] = drift_int(access["denied_entries_last_hour"], 1, 0, 60)
        access["lock_voltage_v"] = round(drift_number(access["lock_voltage_v"], 0.04, 9, 14), 2)
        if random.random() < 0.1:
            access["door_state"] = random.choice(("closed", "open", "forced", "held_open"))
            access["last_credential_result"] = random.choice(("granted", "denied", "expired", "unknown"))

    equipment.readings = readings
    return readings


def get_random_equipment_payload() -> Dict[str, Any]:
    equipment = random.choice(EQUIPMENT)

    equipment.lat = round(drift_number(equipment.lat, 0.00008, -90, 90), 6)
    equipment.long = round(drift_number(equipment.long, 0.00008, -180, 180), 6)
    equipment.battery_level = round(equipment.battery_level - random.uniform(0.4, 1.8), 1)
    if equipment.battery_level <= 0:
        equipment.battery_level = 100.0

    inactive = random.random() < 0.035
    equipment.active = not inactive

    payload: Dict[str, Any] = {
        "ID": equipment.id,
        "type": equipment.type,
        "lat": equipment.lat,
        "long": equipment.long,
        "battery_level": equipment.battery_level,
        "active": equipment.active,
    }

    if inactive:
        payload["data"] = None
        payload["signal"] = "inactive"
    else:
        payload["data"] = update_readings(equipment)
        payload["signal"] = "active"

    return payload


class RequestHandler(BaseHTTPRequestHandler):
    server_version = "BeaconChallengeAPI/1.0"

    def do_GET(self) -> None:
        parsed_path = urlparse(self.path)

        if parsed_path.path != "/data":
            self.send_json({"error": "Not found. Use GET /data."}, status=404)
            return

        self.send_json(get_random_equipment_payload())

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)
    print(f"Serving beacon challenge API at http://{HOST}:{PORT}")
    print("GET /data")
    server.serve_forever()


if __name__ == "__main__":
    main()
