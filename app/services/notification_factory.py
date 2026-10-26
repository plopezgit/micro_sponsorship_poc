# app/services/notification_factory.py
import os
from app.services.notification_service import ConsoleNotificationService
from app.services.sms_notification_service_twilio import SMSNotificationServiceTwilio
from app.services.sms_notification_service_plivo import SMSNotificationServicePlivo

def get_notifier(provider_name: str = None):
    provider = (provider_name or os.getenv("NOTIFICATION_PROVIDER", "console")).lower()

    if provider == "twilio":
        return SMSNotificationServiceTwilio()
    elif provider == "plivo":
        return SMSNotificationServicePlivo()
    else:
        return ConsoleNotificationService()


def get_dual_notifiers():
    """
    Permite configurar un proveedor distinto para usuario y corporativo.
    Ejemplo:
      NOTIFICATION_PROVIDER_USER=twilio
      NOTIFICATION_PROVIDER_PRODUCT=plivo
    """
    user_notifier = get_notifier(os.getenv("NOTIFICATION_PROVIDER_USER"))
    product_notifier = get_notifier(os.getenv("NOTIFICATION_PROVIDER_PRODUCT"))
    return user_notifier, product_notifier
