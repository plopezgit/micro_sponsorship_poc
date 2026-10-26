# app/repositories/app_usage_repository_db.py
from app.db.database import SessionLocal
from app.db.models import AppUsageDB
import datetime

class AppUsageRepositoryDB:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def add_session(self, mobile, session_info):
        s = AppUsageDB(
            user_mobile=mobile,
            start_time=session_info.get("start_time", datetime.datetime.utcnow()),
            duration_minutes=float(session_info.get("duration_minutes", 0)),
            section=session_info.get("section", "")
        )
        self.session.add(s)
        self.session.commit()
        self.session.refresh(s)
        return s

    def get_user_sessions(self, mobile):
        return self.session.query(AppUsageDB).filter(AppUsageDB.user_mobile == mobile).all()

    def get_weekly_median_admin_minutes(self, mobile, reference_date=None):
        # Puedes implementar filtrado por rango como en la versión en memoria
        from statistics import median
        if reference_date is None:
            reference_date = datetime.datetime.utcnow()
        week_start = reference_date - datetime.timedelta(days=reference_date.weekday())
        week_end = week_start + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
        sessions = self.session.query(AppUsageDB).filter(
            AppUsageDB.user_mobile==mobile,
            AppUsageDB.section=="admin",
            AppUsageDB.start_time >= week_start,
            AppUsageDB.start_time <= week_end
        ).all()
        durations = [s.duration_minutes for s in sessions]
        if not durations:
            return 1.0
        return float(median(durations))
