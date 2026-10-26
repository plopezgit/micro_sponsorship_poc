# app/services/sms_notification_service_twilio.py
import os
import logging
from twilio.rest import Client
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

class SMSNotificationServiceTwilio(NotificationService):
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def notify_user(self, user_mobile: str, message: str):
        sms = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=user_mobile
        )
        logger.info(f"[TWILIO SMS] Sent to {user_mobile} | SID={sms.sid}")
