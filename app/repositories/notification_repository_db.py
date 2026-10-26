# app/repositories/notification_repository_db.py
from app.db.database import SessionLocal
from app.db.models import NotificationDB

class NotificationRepositoryDB:
    """
    Repositorio de persistencia para notificaciones (SMS, email, push).
    Permite almacenar y consultar notificaciones enviadas.
    """

    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add_notification(self, user_mobile, message, channel="sms", status="sent"):
        notif = NotificationDB(
            user_mobile=user_mobile,
            message=message,
            channel=channel,
            status=status
        )
        self.session.add(notif)
        self.session.commit()
        self.session.refresh(notif)
        return notif

    def list_by_user(self, user_mobile):
        return self.session.query(NotificationDB).filter_by(user_mobile=user_mobile).all()

    def list_all(self):
        return self.session.query(NotificationDB).all()
