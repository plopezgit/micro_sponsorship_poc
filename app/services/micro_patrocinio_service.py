# app/services/micro_patrocinio_service.py
from typing import Dict
from datetime import datetime
import math
import logging
from app.entities.micro_patrocinio import MicroPatrocinio
from app.repositories.micro_patrocinio_repository_db import MicroPatrocinioRepositoryDB
from app.services.notification_service import NotificationService
from app.services.notification_factory import get_dual_notifiers

logger = logging.getLogger(__name__)

DEFAULT_WEIGHTS = {
    "distancia": 0.4,
    "perfil": 0.3,
    "recurrencia": 0.2,
    "temporalidad": 0.1,
}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class MicroPatrocinioService:
    """
    Servicio que evalúa micro-patrocinios y registra en DB.
    Envía notificaciones si se cumple el umbral.
    """

    def __init__(self, repo: MicroPatrocinioRepositoryDB, notifier_user: NotificationService = None, notifier_product: NotificationService = None):
        self.repo = repo
        self.notifier_user, self.notifier_product = notifier_user, notifier_product
        # fallback a factory dual
        if not (self.notifier_user and self.notifier_product):
            self.notifier_user, self.notifier_product = get_dual_notifiers()

    def calcular_score(self, distancia: float, perfil_u: str, perfil_p: str, delta_minutes: float, frecuencia: int, weights: Dict[str, float] = None):
        weights = weights or DEFAULT_WEIGHTS
        max_dist, max_freq, max_minutes = 1000, 10, 60

        f_dist = max(0, 1 - (distancia / max_dist))
        f_perfil = 1.0 if perfil_u == perfil_p else 0.0
        f_freq = min(frecuencia / max_freq, 1.0)
        f_temp = max(0, 1 - (delta_minutes / max_minutes))

        score = (
            weights["distancia"] * f_dist +
            weights["perfil"] * f_perfil +
            weights["recurrencia"] * f_freq +
            weights["temporalidad"] * f_temp
        )

        return round(score, 4)

    def evaluar_cercania_y_perfil(self, users: Dict[str, dict], products: Dict[str, dict],
                                  umbral_metros: float = 50.0, max_minutes_diff: int = 15,
                                  weights: Dict[str, float] = None):
        for user_id, u_data in (users or {}).items():
            perfil_u = u_data.get("perfil")
            u_checkins = u_data.get("checkins", [])
            if not perfil_u or not u_checkins:
                continue

            for prod_id, p_data in (products or {}).items():
                perfil_p = p_data.get("perfil")
                p_checkins = p_data.get("checkins", [])
                if not perfil_p or not p_checkins:
                    continue

                for u_chk in u_checkins:
                    for p_chk in p_checkins:
                        try:
                            dist = haversine(
                                u_chk["lat"], u_chk["lon"],
                                p_chk["lat"], p_chk["lon"]
                            )
                        except Exception:
                            continue

                        u_time, p_time = u_chk.get("timestamp"), p_chk.get("timestamp")
                        if not isinstance(u_time, datetime) or not isinstance(p_time, datetime):
                            continue

                        delta_minutes = abs((u_time - p_time).total_seconds()) / 60.0
                        frecuencia = len(u_checkins) + len(p_checkins)

                        score = self.calcular_score(dist, perfil_u, perfil_p, delta_minutes, frecuencia, weights)

                        if score > 0.5:
                            if not self.repo.list_by_user(user_id):
                                mp = self.repo.add(user_id, prod_id, score=score)
                                self._notificar(mp)

    def _notificar(self, micro_patrocinio: MicroPatrocinio):
        user_msg = (
            f"Podrías tener un micro-patrocinio con el producto {micro_patrocinio.product_id} "
            f"(score={micro_patrocinio.score})."
        )
        corp_msg = (
            f"Un nuevo usuario {micro_patrocinio.user_mobile} está cerca. "
            f"Potencial micro-patrocinio (score={micro_patrocinio.score})."
        )

        try:
            self.notifier_user.notify_user(micro_patrocinio.user_mobile, user_msg)
            self.notifier_product.notify_product(micro_patrocinio.product_id, corp_msg)
        except Exception as e:
            logger.error(f"Error enviando notificaciones: {e}")
