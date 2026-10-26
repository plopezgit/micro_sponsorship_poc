import math
from typing import Tuple
from geopy.distance import geodesic

def calculate_haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calcula la distancia en metros entre dos puntos geográficos (latitud, longitud).
    Utiliza geopy para máxima precisión geográfica.
    """
    return geodesic(coord1, coord2).meters

def is_valid_coordinate(lat: float, lon: float) -> bool:
    """
    Valida si las coordenadas están dentro de los rangos globales válidos.
    """
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0