# app/services/micro_patrocinio_evaluator.py
import logging
from geopy.distance import geodesic
from app.services.micro_patrocinio_service import MicroPatrocinioService

logger = logging.getLogger(__name__)

class MicroPatrocinioEvaluator:
    def __init__(self, user_repo, product_repo, micro_service: MicroPatrocinioService):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.micro_service = micro_service

    def _get_users(self):
        if hasattr(self.user_repo, "export_for_evaluator"):
            return self.user_repo.export_for_evaluator()
        elif hasattr(self.user_repo, "users"):
            return {
                u_id: {"checkins": u.checkins or [], "perfil": u.perfil}
                for u_id, u in self.user_repo.users.items()
            }
        return {}

    def _get_products(self):
        if hasattr(self.product_repo, "export_for_evaluator"):
            return self.product_repo.export_for_evaluator()
        elif hasattr(self.product_repo, "products"):
            return {
                p_id: {"checkins": p.checkins or [], "perfil": p.perfil}
                for p_id, p in self.product_repo.products.items()
            }
        return {}

    def calcular_distancia_maxima(self, users, products):
        max_dist = 0
        for u_obj in users.values():
            for p_obj in products.values():
                for u_ck in u_obj.get("checkins", []):
                    for p_ck in p_obj.get("checkins", []):
                        dist = geodesic(
                            (u_ck["lat"], u_ck["lon"]),
                            (p_ck["lat"], p_ck["lon"])
                        ).meters
                        max_dist = max(max_dist, dist)
        return max_dist

    def run_evaluation(self, umbral_metros: float = None, max_minutes_diff: float = 15):
        users = self._get_users()
        products = self._get_products()

        if umbral_metros is None:
            max_dist = self.calcular_distancia_maxima(users, products)
            umbral_metros = max_dist + 5
            logger.info(f"Umbral calculado automáticamente: {umbral_metros:.2f} metros")

        self.micro_service.evaluar_cercania_y_perfil(
            users,
            products,
            umbral_metros=umbral_metros,
            max_minutes_diff=max_minutes_diff
            
        )


