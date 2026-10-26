# app/repositories/product_repository_db.py
from sqlalchemy import text
from app.db.database import SessionLocal
from app.db.models import ProductDB

class ProductRepositoryDB:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add_product(self, product_id: str, name: str, company: str, perfil: str):
        dbp = ProductDB(
            product_id=product_id,
            name=name,
            company=company,
            perfil=perfil,
        )
        self.session.add(dbp)
        self.session.commit()
        self.session.refresh(dbp)
        return dbp

    def get_product(self, product_id: str):
        return self.session.get(ProductDB, product_id)

    def list_products(self):
        return self.session.query(ProductDB).all()

    def export_for_evaluator(self) -> dict:
        result = {}
        products = self.list_products()
        for p in products:
            query = text("""
                SELECT lat, lon, created_at 
                FROM checkins 
                WHERE user_id = :pid AND tipo = 'product'
            """)
            db_checkins = self.session.execute(query, {"pid": p.product_id}).fetchall()
            
            checkins = [
                {"lat": row.lat, "lon": row.lon, "timestamp": row.created_at}
                for row in db_checkins
            ]
            result[p.product_id] = {
                "checkins": checkins,
                "perfil": p.perfil
            }
        return result