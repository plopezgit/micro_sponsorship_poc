# app/entities/ciclo.py
from dataclasses import dataclass
from datetime import datetime
import math

@dataclass
class Ciclo:
    user_id: str
    product_id: str
    checkin_lat: float
    checkin_lon: float
    checkin_time: datetime
    checkout_lat: float
    checkout_lon: float
    checkout_time: datetime

    @property
    def duration_seconds(self) -> float:
        return (self.checkout_time - self.checkin_time).total_seconds()

    def distance_meters(self) -> float:
        """Calcula distancia entre check-in y check-out usando fórmula Haversine"""
        R = 6371000  # Radio Tierra en metros
        phi1, phi2 = math.radians(self.checkin_lat), math.radians(self.checkout_lat)
        delta_phi = math.radians(self.checkout_lat - self.checkin_lat)
        delta_lambda = math.radians(self.checkout_lon - self.checkin_lon)
        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
