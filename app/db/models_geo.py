import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from geoalchemy2 import Geometry, Geography
from app.db.models import Base

class ZonaDB(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=True)  # comercial, residencial, etc.
    geom = Column(Geometry("POLYGON", srid=4326))  # polígono geográfico

class CheckinDB(Base):
    __tablename__ = "checkins"

    # Mapeado exacto al DDL de Supabase: id text, user_id, status, location, timestamp
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_mobile = Column("user_id", String, ForeignKey("users.mobile"), nullable=False)
    tipo = Column("status", String, nullable=False)
    location = Column(Geography("POINT", srid=4326))
    timestamp = Column(DateTime(timezone=True), nullable=False)