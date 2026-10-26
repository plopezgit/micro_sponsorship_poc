import bcrypt
import logging
from typing import Optional, Union
from app.repositories.user_repository_db import UserRepositoryDB
from app.repositories.user_repo import UserRepository
from app.entities.user import User
from app.db.models import UserDB

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, user_repo: Union[UserRepositoryDB, UserRepository]):
        self.user_repo = user_repo

    def _hash_password(self, password: str) -> str:
        """Genera un hash seguro utilizando bcrypt"""
        password_bytes = password[:72].encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado"""
        try:
            password_bytes = plain_password[:72].encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            logger.error(f"Error al verificar contraseña: {e}")
            return False

    def register(self, mobile: str, password: str, perfil: Optional[str] = None) -> bool:
        """Registra un nuevo usuario con contraseña hasheada en bcrypt"""
        if self.user_repo.get_user(mobile):
            return False

        hashed_pw = self._hash_password(password)

        if isinstance(self.user_repo, UserRepositoryDB):
            new_user = User(mobile=mobile, password_hash=hashed_pw, perfil=perfil)
            self.user_repo.add_user(new_user)
        else:
            new_user = User(mobile=mobile, password_hash=hashed_pw, perfil=perfil, checkins=[])
            self.user_repo.add_user(new_user)

        return True

    def login(self, mobile: str, password: str) -> Optional[dict]:
        """
        Valida credenciales y retorna los datos del usuario si es exitoso,
        o None si falla.
        """
        user = self.user_repo.get_user(mobile)
        if not user:
            return None

        # Obtener hash de contraseña (Soporta modelo ORM y Dataclass)
        stored_hash = getattr(user, "password_hash", None)
        if not stored_hash or not self._verify_password(password, stored_hash):
            return None

        # Formatear respuesta del usuario
        return {
            "mobile": user.mobile,
            "perfil": getattr(user, "perfil", None)
        }