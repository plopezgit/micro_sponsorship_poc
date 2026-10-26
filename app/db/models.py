# app/db/models.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime
import math

class UserDB(Base):
    __tablename__ = "users"

    mobile = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    perfil = Column(String, nullable=True)

    # Relaciones
    ciclos = relationship("CicloDB", back_populates="user")
    app_sessions = relationship("AppUsageDB", back_populates="user")
    invites = relationship("InvitationDB", back_populates="user")

class ProductDB(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    perfil = Column(String, nullable=True)

    # Relaciones
    ciclos = relationship("CicloDB", back_populates="product")


class CicloDB(Base):
    __tablename__ = "ciclos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.mobile"), index=True)
    product_id = Column(String, ForeignKey("products.product_id"), index=True)
    checkin_lat = Column(Float)
    checkin_lon = Column(Float)
    checkin_time = Column(DateTime, default=datetime.datetime.utcnow)
    checkout_lat = Column(Float)
    checkout_lon = Column(Float)
    checkout_time = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserDB", back_populates="ciclos")
    product = relationship("ProductDB", back_populates="ciclos")

    @property
    def duration_seconds(self) -> float:
        if self.checkin_time and self.checkout_time:
            return (self.checkout_time - self.checkin_time).total_seconds()
        return 0.0

    def distance_meters(self) -> float:
        if any(v is None for v in (self.checkin_lat, self.checkin_lon, self.checkout_lat, self.checkout_lon)):
            return 0.0
        R = 6371000
        phi1 = math.radians(self.checkin_lat)
        phi2 = math.radians(self.checkout_lat)
        delta_phi = math.radians(self.checkout_lat - self.checkin_lat)
        delta_lambda = math.radians(self.checkout_lon - self.checkin_lon)
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c


class AppUsageDB(Base):
    __tablename__ = "app_usage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_mobile = Column(String, ForeignKey("users.mobile"), index=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    duration_minutes = Column(Float, default=0.0)
    section = Column(String, default="")

    user = relationship("UserDB", back_populates="app_sessions")


class InvitationDB(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_mobile = Column(String, ForeignKey("users.mobile"), index=True)
    invited_user = Column(String)
    invite_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserDB", back_populates="invites")


class MicroPatrocinioDB(Base):
    __tablename__ = "micropatrocinios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_mobile = Column(String, ForeignKey("users.mobile"), index=True)
    product_id = Column(String, ForeignKey("products.product_id"), index=True)
    score = Column(Float, default=0.0)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class NotificationDB(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_mobile = Column(String, index=True)
    message = Column(String)
    channel = Column(String, default="sms")
    status = Column(String, default="sent")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)