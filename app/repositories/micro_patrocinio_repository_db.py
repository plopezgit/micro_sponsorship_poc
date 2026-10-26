from app.db.database import SessionLocal
from app.db.models import MicroPatrocinioDB

class MicroPatrocinioRepositoryDB:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add(self, user_mobile, product_id, score=0.0, status="pending"):
        m = MicroPatrocinioDB(
            user_mobile=user_mobile,
            product_id=product_id,
            score=score,
            status=status
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def list_all(self):
        return self.session.query(MicroPatrocinioDB).all()

    def list_by_user(self, user_mobile: str):
        """Devuelve todos los micropatrocinios de un usuario."""
        return self.session.query(MicroPatrocinioDB).filter(
            MicroPatrocinioDB.user_mobile == user_mobile
        ).all()

    def update_status(self, microp_id: int, new_status: str):
        """Actualiza el estado de un micropatrocinio y lo devuelve."""
        m = self.session.get(MicroPatrocinioDB, microp_id)
        if not m:
            return None
        m.status = new_status
        self.session.commit()
        self.session.refresh(m)
        return m
