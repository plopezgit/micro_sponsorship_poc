# Micro-sponsorship System

Python backend project for detecting and managing **proximity-based micro-sponsorships** between users and corporate products, implemented under **Clean Architecture** using FastAPI, PostgreSQL, and SQLAlchemy.

## Features
- User registration & login with mobile numbers and passwords.
- Product registration with profiles (e.g., "Deporte").
- Location-based check-ins for users and products stored directly in PostgreSQL.
- Decoupled repositories with `export_for_evaluator` methods for direct data extraction.
- Evaluation of potential **micro-sponsorships** using composite scoring:
  - Distance (Haversine formula)
  - Profile affinity
  - User recurrence
  - Temporal proximity (`max_minutes_diff`)
- Notification system for detected sponsorships.
- PostgreSQL and SQLAlchemy-based persistence layer.

---

## Core Workflow

1. **Check-in:** A user or product records their location via FastAPI endpoints.  
2. **Repository Export:** `UserRepositoryDB` and `ProductRepositoryDB` export check-ins via direct database queries.  
3. **Micro-sponsorship evaluation:**  
   The `MicroPatrocinioEvaluator` and `MicroPatrocinioService` analyze proximity, time, and apply the scoring model.  
4. **Persistence & Notification:**  
   Persists the result in PostgreSQL, triggers notifications, and maintains sponsorship status.

---

## Composite Score Logic

Each potential sponsorship is evaluated using a weighted score:

```
Score = (DistanceWeight * f(distance)) +
        (ProfileWeight * profile_match) +
        (RecurrenceWeight * user_frequency) +
        (TemporalWeight * time_window)

**Weights (default):**
DEFAULT_WEIGHTS = {
    "distancia": 0.4,
    "perfil": 0.3,
    "recurrencia": 0.2,
    "temporalidad": 0.1,
}
```

- Distance: closer = higher score.
- Profile: measures how well user and product profiles align.
- Recurrence: frequency of repeated proximity events.
- Temporal: evaluates how recent the check-ins occurred.

A sponsorship is created when the total score exceeds a threshold (e.g., 0.5).

---

## Conceptual Diagram

*Actualizado: 07/10/2025*

```
[User / Product] 
        |
        |--- POST /api/checkin (lat, lon)
        v
[PostgreSQL Database (checkins table)]
        |
        |--- GET export_for_evaluator()
        v
[UserRepositoryDB & ProductRepositoryDB]
        |
        v
[MicroPatrocinioEvaluator]
        |
        v
[MicroPatrocinioService (Haversine & Scoring)]
        |
        v
[PostgreSQL Database (micropatrocinios table)]
        |
        v
[NotificationService (Dual Notifiers)]
        |
        v
Console / SMS output

Example message:
[USER] 5551234567 → "You might have a micro-sponsorship with prod001 (score=0.78)"
[CORP] prod001     → "New user detected with score=0.78"
```

---

## Project Structure
```
project_root/
├── app/
│   ├── api/routes/     # FastAPI endpoints (auth, checkin, evaluator)
│   ├── db/             # Database connection and SQLAlchemy models
│   ├── entities/       # Domain entities
│   ├── repositories/   # Database repositories with evaluator exports
│   ├── services/       # Business logic and evaluator
│   └── main.py         # FastAPI application entry point
├── app/test/           # Unit tests
├── requirements.txt
└── README.md
```

---

## Installation & Usage
```bash
git clone <repo_url>
cd project_root
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

---

## Notes & Future Improvements

- android client MVP
- [advanced fraud mitigation for proximity cycles notes](docs/riesgos_fraude_ciclos.md)   
  

---

## License
MIT License
