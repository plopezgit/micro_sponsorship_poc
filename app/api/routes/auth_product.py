from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_product_service import AuthProductService  # <--- Importante

router = APIRouter(prefix="/api", tags=["Auth & Products"])

class UserRegisterSchema(BaseModel):
    mobile: str
    password: str
    name: str | None = None
    profile: str | None = "standard"

class UserLoginSchema(BaseModel):
    mobile: str
    password: str

class ProductRegisterSchema(BaseModel):
    product_id: str
    name: str
    company: str | None = None
    profile: str

@router.post("/auth/register")
def register_user(data: UserRegisterSchema, db: Session = Depends(get_db)):
    try:
        service = AuthProductService(session=db)
        user = service.register_user(
            mobile=data.mobile, 
            password=data.password, 
            name=data.name, 
            profile=data.profile
        )
        return {"status": "ok", "message": "Usuario registrado exitosamente", "mobile": user.mobile}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/auth/login")
def login(data: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        service = AuthProductService(session=db)
        token = service.authenticate_user(mobile=data.mobile, password=data.password)
        return {
            "status": "ok",
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/products/register")
def register_product(data: ProductRegisterSchema, db: Session = Depends(get_db)):
    try:
        service = AuthProductService(session=db)
        product = service.register_product(
            product_id=data.product_id,
            name=data.name,
            company=data.company,
            profile=data.profile
        )
        # Ojo aquí: usar product.product_id en vez de product.id
        return {"status": "ok", "message": "Producto registrado exitosamente", "product_id": product.product_id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")