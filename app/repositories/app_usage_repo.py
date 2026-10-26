# app/repositories/app_usage_repo.py
from datetime import datetime, timedelta
import statistics

class AppUsageRepository:
    """
    Repositorio en memoria para sesiones de app de usuarios.
    Cada usuario identificado por mobile tiene una lista de sesiones (dict).
    """
    def __init__(self):
        self.sessions = {}  # dict[str, list[dict]]

    def add_session(self, mobile, session_info):
        """
        Agrega una sesión para un usuario identificado por mobile.
        session_info: dict con detalles de la sesión (start_time, duration_minutes, section, etc.)
        """
        if mobile not in self.sessions:
            self.sessions[mobile] = []
        self.sessions[mobile].append(session_info)

    def get_user_sessions(self, mobile):
        """
        Retorna todas las sesiones de un usuario.
        """
        return self.sessions.get(mobile, [])

    def get_all_sessions(self):
        """
        Retorna todas las sesiones de todos los usuarios.
        """
        return self.sessions

    # -----------------------------
    # NUEVO MÉTODO: mediana semanal para secciones administrativas
    # -----------------------------
    def get_weekly_median_admin_minutes(self, mobile, reference_date=None):
        """
        Calcula la mediana de minutos semanales en sesiones de secciones administrativas
        para un usuario dado.

        reference_date: datetime para considerar "esta semana", default = hoy.
        """
        if reference_date is None:
            reference_date = datetime.now()

        one_week_ago = reference_date - timedelta(days=7)
        sessions = self.get_user_sessions(mobile)
        admin_durations = [
            s.get("duration_minutes", 0)
            for s in sessions
            if s.get("section") == "admin" and one_week_ago <= s.get("start_time", reference_date) <= reference_date
        ]

        if not admin_durations:
            return 1  # Para evitar división por cero en la fórmula
        return statistics.median(admin_durations)
