from dataclasses import dataclass

@dataclass
class MicroPatrocinio:
    user_id: str
    corp_id: str
    status: str = "pending"