# app/api/routes/checkin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.checkin_service import CheckinService

router = APIRouter(prefix="/api")

@router.post("/checkin")
def checkin(mobile: str, tipo: str, lat: float, lon: float, db: Session = Depends(get_db)):
    try:
        service = CheckinService(session=db)
        result = service.record_checkin(mobile=mobile, tipo=tipo, lat=lat, lon=lon)
        
        return {
            "status": "ok",
            "checkin_id": result["checkin_id"],
            "zona": result["zona"]
        }
    except ValueError as ve:
        # Errores de validación de negocio (usuario/producto no existe, tipo inválido)
        db.rollback()
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        # Errores técnicos inesperados de base de datos
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registrando checkin: {str(e)}")