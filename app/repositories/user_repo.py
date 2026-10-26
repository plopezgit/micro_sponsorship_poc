from sqlalchemy.orm import Session
from app.repositories.user_product_repository import UserProductRepository
from app.core.security import hash_password, verify_password, create_access_token

class AuthProductService:
    def __init__(self, session: Session):
        self.repo = UserProductRepository(session=session)

    def register_user(self, mobile: str, password: str, name: str = None, profile: str = "standard"):
        existing_user = self.repo.get_user_by_mobile(mobile)
        if existing_user:
            raise ValueError(f"El usuario con móvil '{mobile}' ya está registrado.")
        
        hashed_pwd = hash_password(password)
        return self.repo.create_user(
            mobile=mobile, 
            password_hash=hashed_pwd, 
            name=name, 
            profile=profile
        )

    def authenticate_user(self, mobile: str, password: str) -> str:
        user = self.repo.get_user_by_mobile(mobile)
        if not user or not verify_password(password, user.password):
            raise ValueError("Credenciales inválidas. Número de móvil o contraseña incorrectos.")
        
        access_token = create_access_token(data={"sub": user.mobile})
        return access_token

    def register_product(self, product_id: str, name: str, company: str, profile: str):
        existing_product = self.repo.get_product_by_id(product_id)
        if existing_product:
            raise ValueError(f"El producto con ID '{product_id}' ya está registrado.")

        return self.repo.create_product(
            product_id=product_id,
            name=name,
            company=company,
            profile=profile
        )