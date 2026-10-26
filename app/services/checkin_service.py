# app/services/checkin_service.py
from sqlalchemy.orm import Session
from app.db.models import UserDB, ProductDB
from app.repositories.checkin_repository_db import CheckinRepositoryDB

class CheckinService:
    def __init__(self, session: Session):
        self.session = session
        self.checkin_repo = CheckinRepositoryDB(session=session)

    def record_checkin(self, mobile: str, tipo: str, lat: float, lon: float):
        # 1. Regla de negocio: Validar existencia de la entidad
        if tipo == "user":
            if not self.session.get(UserDB, mobile):
                raise ValueError(f"El usuario con identificador '{mobile}' no está registrado.")
        elif tipo == "product":
            if not self.session.get(ProductDB, mobile):
                raise ValueError(f"El producto con identificador '{mobile}' no está registrado.")
        else:
            raise ValueError("El parámetro 'tipo' debe ser estrictamente 'user' o 'product'.")

        try:
            # 2. Delegar la persistencia al repositorio
            checkin_id = self.checkin_repo.create(mobile=mobile, tipo=tipo, lat=lat, lon=lon)
            
            # 3. Consultar zona geográfica
            zona_nombre = self.checkin_repo.get_zone_by_coords(lat=lat, lon=lon)

            self.session.commit()

            return {
                "checkin_id": checkin_id,
                "zona": zona_nombre
            }
        except Exception as e:
            self.session.rollback()
            raise e