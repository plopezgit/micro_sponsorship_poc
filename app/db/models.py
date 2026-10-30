# app/db/models.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class UserDB(Base):
    __tablename__ = "users"

    mobile = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    perfil = Column(String, nullable=True)

class ProductDB(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    perfil = Column(String, nullable=True)

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