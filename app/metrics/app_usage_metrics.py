from statistics import median
from datetime import datetime

class AppUsageMetrics:
    """
    Extrae métricas de uso de la app por usuario.
    """

    def __init__(self, app_usage_repo):
        self.app_usage_repo = app_usage_repo

    def _filter_sessions(self, user, week_start=None, week_end=None):
        # Llamada corregida al método real del repositorio
        sessions = self.app_usage_repo.get_user_sessions(user)
        week_start = week_start or datetime.min
        week_end = week_end or datetime.max
        
        filtered = []
        for s in sessions:
            # Soporte dual: acceso por atributo (ORM/Dataclass) o por clave (Dict)
            start_time = getattr(s, 'start_time', None) if not isinstance(s, dict) else s.get('start_time')
            if start_time and week_start <= start_time <= week_end:
                filtered.append(s)
                
        return filtered

    def get_weekly_median_minutes(self, user, week_start=None, week_end=None):
        sessions = self._filter_sessions(user, week_start, week_end)
        
        # Obtener duración soportando atributos u objetos diccionarios
        minutes = [
            getattr(s, 'duration_minutes', 0) if not isinstance(s, dict) else s.get('duration_minutes', 0)
            for s in sessions
        ]
        
        if not minutes:
            return 0.0
        return float(median(minutes))