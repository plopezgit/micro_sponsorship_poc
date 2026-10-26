from dataclasses import dataclass, field

@dataclass
class User:
    mobile: str
    password_hash: str
    checkins: list = field(default_factory=list)  # <-- inicializa como lista vacía
    perfil: str = None         # Perfil del usuario, e.g., "Runner", "Cyclist"
