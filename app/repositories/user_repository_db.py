# app/repositories/user_repository_db.py
from sqlalchemy import text
from app.db.database import SessionLocal
from app.db.models import UserDB

class UserRepositoryDB:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add_user(self, mobile: str, password_hash: str, name: str = None, perfil: str = "standard"):
        db_user = UserDB(
            mobile=mobile,
            password_hash=password_hash,
            name=name,
            perfil=perfil
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user(self, mobile: str):
        return self.session.get(UserDB, mobile)

    def list_users(self):
        return self.session.query(UserDB).all()

    def export_for_evaluator(self) -> dict:
        result = {}
        users = self.list_users()
        for u in users:
            query = text("""
                SELECT lat, lon, created_at 
                FROM checkins 
                WHERE user_id = :mobile AND tipo = 'user'
            """)
            db_checkins = self.session.execute(query, {"mobile": u.mobile}).fetchall()
            
            checkins = [
                {"lat": row.lat, "lon": row.lon, "timestamp": row.created_at}
                for row in db_checkins
            ]
            result[u.mobile] = {
                "checkins": checkins,
                "perfil": u.perfil
            }
        return result