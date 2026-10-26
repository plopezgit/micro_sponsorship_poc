import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener URL de base de datos desde entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()

def get_db():
    """Generador de sesiones para inyección de dependencias en FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa las tablas definidas en los modelos ORM"""
    Base.metadata.create_all(bind=engine)