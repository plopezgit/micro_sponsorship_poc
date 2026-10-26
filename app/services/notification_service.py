# app/services/notification_service.py
import logging
logger = logging.getLogger(__name__)

class NotificationService:
    """Interfaz base para notificaciones."""
    def notify_user(self, user_mobile: str, message: str):
        raise NotImplementedError

    def notify_product(self, product_id: str, message: str):
        raise NotImplementedError


class ConsoleNotificationService(NotificationService):
    """Mock para desarrollo y tests."""

    def notify_user(self, user_mobile: str, message: str):
        logger.info(f"[USER-CONSOLE] {user_mobile}: {message}")

    def notify_product(self, product_id: str, message: str):
        logger.info(f"[CORP-CONSOLE] {product_id}: {message}")
