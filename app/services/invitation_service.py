# app/services/invitation_service.py
from app.repositories.invitation_repository_db import InvitationRepositoryDB
from app.repositories.notification_repository_db import NotificationRepositoryDB
from app.services.notification_factory import get_notifier

class InvitationService:
    """
    Servicio que maneja la lógica de invitaciones de usuarios.
    Integra el sistema de notificaciones SMS con persistencia.
    """

    def __init__(self, invitation_repo: InvitationRepositoryDB, notification_repo: NotificationRepositoryDB, notifier=None):
        self.invitation_repo = invitation_repo
        self.notification_repo = notification_repo
        self.notifier = notifier or get_notifier()

    def send_invitation(self, inviter_mobile: str, invitee_mobile: str):
        """
        Envía una invitación de un usuario a otro, notificando y persistiendo el evento.
        """
        # 1️⃣ Crear la invitación en base de datos
        invite = self.invitation_repo.add_invite(inviter_mobile, invitee_mobile)

        # 2️⃣ Preparar y enviar mensaje SMS (o consola según configuración)
        message = f"¡{inviter_mobile} te ha invitado a unirte a nuestra app! Usa tu número {invitee_mobile} para registrarte."
        self.notifier.notify_user(invitee_mobile, message)

        # 3️⃣ Registrar la notificación en base de datos
        self.notification_repo.add_notification(
            user_mobile=invitee_mobile,
            message=message,
            channel="sms",
            status="sent"
        )

        return invite

    def get_user_invites(self, user_mobile: str):
        """
        Devuelve todas las invitaciones enviadas por un usuario.
        """
        return self.invitation_repo.get_user_invites(user_mobile)

    def get_user_notifications(self, user_mobile: str):
        """
        Devuelve las notificaciones asociadas al usuario (historial).
        """
        return self.notification_repo.list_by_user(user_mobile)
