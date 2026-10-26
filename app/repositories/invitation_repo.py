from typing import List, Dict
from datetime import datetime, timedelta

class InvitationRepository:
    """Repositorio in-memory de invitaciones"""

    def __init__(self):
        # Estructura: {user_mobile: List[{'invite_date': datetime, 'invited_user': str}]}
        self.invites: Dict[str, List[dict]] = {}

    def add_invite(self, user_mobile: str, invited_user: str, invite_date: datetime):
        """
        Registra una nueva invitación para un usuario.
        Mantiene compatibilidad con código previo.
        """
        if user_mobile not in self.invites:
            self.invites[user_mobile] = []
        self.invites[user_mobile].append({"invite_date": invite_date, "invited_user": invited_user})

    def get_user_invites(self, user_mobile: str) -> List[dict]:
        """
        Retorna todas las invitaciones de un usuario.
        Mantiene compatibilidad con código previo.
        """
        return self.invites.get(user_mobile, [])


