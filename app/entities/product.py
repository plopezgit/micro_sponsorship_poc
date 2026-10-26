from dataclasses import dataclass, field

@dataclass
class Product:
    product_id: str
    name: str
    company: str
    checkins: list = field(default_factory=list)  # <-- inicializa como lista vacía
    perfil: str = None         # Perfil del producto, e.g., "Runner", "Cyclist"