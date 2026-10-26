# app/services/sms_notification_service_plivo.py
import os
import logging
import plivo
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

class SMSNotificationServicePlivo(NotificationService):
    def __init__(self):
        self.auth_id = os.getenv("PLIVO_AUTH_ID")
        self.auth_token = os.getenv("PLIVO_AUTH_TOKEN")
        self.from_number = os.getenv("PLIVO_PHONE_NUMBER")
        self.client = plivo.RestClient(self.auth_id, self.auth_token)

    def notify_user(self, user_mobile: str, message: str):
        response = self.client.messages.create(
            src=self.from_number,
            dst=user_mobile,
            text=message
        )
        logger.info(f"[PLIVO SMS] Sent to {user_mobile} | Message UUID={response['message_uuid']}")
