from typing import List, Dict, Tuple

class ZoneRepository:
    def __init__(self):
        self.zones = {}

    def add_zone(self, zone_id: str, center: Tuple[float, float], radius_m: float) -> None:
        self.zones[zone_id] = {"zone_id": zone_id, "center": center, "radius_m": radius_m}

    def get_zones(self) -> List[Dict]:
        return list(self.zones.values())