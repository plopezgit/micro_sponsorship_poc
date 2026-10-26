# app/api/routes/evaluator.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories.micro_patrocinio_repository_db import MicroPatrocinioRepositoryDB
from app.repositories.user_repository_db import UserRepositoryDB
from app.repositories.product_repository_db import ProductRepositoryDB
from app.services.micro_patrocinio_service import MicroPatrocinioService
from app.services.micro_patrocinio_evaluator import MicroPatrocinioEvaluator

router = APIRouter(prefix="/api/evaluator", tags=["Evaluator"])

@router.post("/evaluate")
def run_evaluation_endpoint(
    umbral_metros: float = Query(None, description="Umbral de distancia opcional en metros"),
    max_minutes_diff: float = Query(15.0, description="Diferencia máxima en minutos"),
    db: Session = Depends(get_db)
):
    try:
        # 1. Instanciar los repositorios correctos
        patrocinio_repo = MicroPatrocinioRepositoryDB(session=db)
        user_repo = UserRepositoryDB(session=db)
        product_repo = ProductRepositoryDB(session=db)
        
        service = MicroPatrocinioService(repo=patrocinio_repo)
        
        # 2. Inyectar los repositorios correspondientes al evaluador
        evaluator = MicroPatrocinioEvaluator(
            user_repo=user_repo, 
            product_repo=product_repo, 
            micro_service=service
        )
        
        # 3. Ejecutar evaluación en tiempo real con los datos de la BD
        evaluator.run_evaluation(
            umbral_metros=umbral_metros, 
            max_minutes_diff=max_minutes_diff
        )
        
        # 4. Retornar patrocinios actualizados
        patrocinios = patrocinio_repo.list_all()
        return {
            "status": "ok",
            "message": "Evaluación completada con éxito",
            "total_patrocinios": len(patrocinios),
            "patrocinios": [
                {
                    "id": p.id,
                    "user_mobile": p.user_mobile,
                    "product_id": p.product_id,
                    "score": p.score,
                    "status": p.status
                }
                for p in patrocinios
            ]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la evaluación: {str(e)}")