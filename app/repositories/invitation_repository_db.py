from app.db.database import SessionLocal
from app.db.models import InvitationDB
import datetime

class InvitationRepositoryDB:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add_invite(self, user_mobile, invited_user, invite_date=None):
        invite_date = invite_date or datetime.datetime.utcnow()
        i = InvitationDB(
            user_mobile=user_mobile,
            invited_user=invited_user,
            invite_date=invite_date
        )
        self.session.add(i)
        self.session.commit()
        self.session.refresh(i)
        return i

    def get_user_invites(self, user_mobile):
        """
        Devuelve TODAS las invitaciones del usuario como objetos InvitationDB
        """
        return self.session.query(InvitationDB).filter(
            InvitationDB.user_mobile == user_mobile
        ).all()

    def get_active_invitations(self, user_mobile, reference_date=None):
        """
        Devuelve objetos InvitationDB correspondientes a los últimos 7 días
        """
        reference_date = reference_date or datetime.datetime.utcnow()
        one_week_ago = reference_date - datetime.timedelta(days=7)

        return self.session.query(InvitationDB).filter(
            InvitationDB.user_mobile == user_mobile,
            InvitationDB.invite_date >= one_week_ago,
            InvitationDB.invite_date <= reference_date
        ).all()

    def get_weekly_entries(self, user_mobile, reference_date=None):
        """
        Devuelve objetos InvitationDB de la última semana (para métricas).
        La lógica de contar o promediar se hace en InvitationMetrics.
        """
        return self.get_active_invitations(user_mobile, reference_date)
