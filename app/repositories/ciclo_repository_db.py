# app/repositories/ciclo_repository_db.py
from app.db.database import SessionLocal
from app.db.models import CicloDB

class CicloRepositoryDB:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add_cycle(self, user_id, product_id, checkin_lat, checkin_lon, checkin_time,
                  checkout_lat, checkout_lon, checkout_time):
        c = CicloDB(
            user_id=user_id, product_id=product_id,
            checkin_lat=checkin_lat, checkin_lon=checkin_lon, checkin_time=checkin_time,
            checkout_lat=checkout_lat, checkout_lon=checkout_lon, checkout_time=checkout_time
        )
        self.session.add(c)
        self.session.commit()
        self.session.refresh(c)
        return c

    def get_all(self):
        return self.session.query(CicloDB).all()

    def get_by_user(self, user_mobile):
        return self.session.query(CicloDB).filter(CicloDB.user_id == user_mobile).all()
