# app/repositories/checkin_repository_db.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

class CheckinRepositoryDB:
    def __init__(self, session: Session):
        self.session = session

    def create(self, mobile: str, tipo: str, lat: float, lon: float) -> str:
        checkin_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        insert_query = text("""
            INSERT INTO checkins (id, user_id, tipo, lat, lon, created_at, geom)
            VALUES (:id, :mobile, :tipo, :lat, :lon, :created_at, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
        """)
        
        self.session.execute(insert_query, {
            "id": checkin_id,
            "mobile": mobile,
            "tipo": tipo,
            "lat": lat,
            "lon": lon,
            "created_at": now
        })
        return checkin_id

    def get_zone_by_coords(self, lat: float, lon: float) -> str | None:
        try:
            query = text("""
                SELECT nombre 
                FROM zonas 
                WHERE ST_Intersects(geom, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
                LIMIT 1;
            """)
            result = self.session.execute(query, {"lon": lon, "lat": lat}).fetchone()
            return result[0] if result else None
        except Exception:
            return None