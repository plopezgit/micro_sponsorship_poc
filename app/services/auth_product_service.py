from sqlalchemy.orm import Session
from app.repositories.user_repository_db import UserRepositoryDB
from app.repositories.product_repository_db import ProductRepositoryDB
from app.core.security import hash_password, verify_password, create_access_token

class AuthProductService:
    def __init__(self, session: Session):
        self.user_repo = UserRepositoryDB(session=session)
        self.product_repo = ProductRepositoryDB(session=session)

    def register_user(self, mobile: str, password: str, name: str = None, profile: str = "standard"):
        existing_user = self.user_repo.get_user_by_mobile(mobile) if hasattr(self.user_repo, "get_user_by_mobile") else self.user_repo.get_user(mobile)
        if existing_user:
            raise ValueError(f"El usuario con móvil '{mobile}' ya está registrado.")
        
        hashed_pwd = hash_password(password)
        
        # Crear usuario usando el modelo ORM directamente o el método del repo
        from app.db.models import UserDB
        db_user = UserDB(
            mobile=mobile,
            password_hash=hashed_pwd,
            name=name,
            perfil=profile
        )
        self.user_repo.session.add(db_user)
        self.user_repo.session.commit()
        self.user_repo.session.refresh(db_user)
        return db_user

    def authenticate_user(self, mobile: str, password: str) -> str:
        user = self.user_repo.get_user(mobile)
        
        # Cambiar user.password por user.password_hash
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Credenciales inválidas. Número de móvil o contraseña incorrectos.")
        
        access_token = create_access_token(data={"sub": user.mobile})
        return access_token

    def register_product(self, product_id: str, name: str, company: str, profile: str):
        existing_product = self.product_repo.get_product(product_id)
        if existing_product:
            raise ValueError(f"El producto con ID '{product_id}' ya está registrado.")

        return self.product_repo.add_product(
            product_id=product_id,
            name=name,
            company=company,
            perfil=profile
        )
        self.product_repo.session.add(dbp)
        self.product_repo.session.commit()
        self.product_repo.session.refresh(dbp)
        return dbp