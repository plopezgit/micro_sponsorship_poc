# app/repositories/ciclo_repo.py
from app.entities.ciclo import Ciclo

class CicloRepository:
    """
    Repositorio en memoria para ciclos de check-in/check-out.
    """

    def __init__(self):
        self.cycles = []  # lista de Ciclo

    def add_cycle(self, user_id, product_id, checkin_lat, checkin_lon, checkin_time,
                  checkout_lat, checkout_lon, checkout_time):
        """
        Crea un ciclo y lo almacena.
        Retorna el objeto Ciclo creado.
        """
        ciclo = Ciclo(
            user_id=user_id,
            product_id=product_id,
            checkin_lat=checkin_lat,
            checkin_lon=checkin_lon,
            checkin_time=checkin_time,
            checkout_lat=checkout_lat,
            checkout_lon=checkout_lon,
            checkout_time=checkout_time
        )
        self.cycles.append(ciclo)
        return ciclo

    def get_all(self):
        """
        Retorna todos los ciclos.
        """
        return self.cycles
