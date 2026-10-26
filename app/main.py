import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import init_db
from app.api.routes import checkin, evaluator, auth_product  # <--- Importar auth_product

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa las tablas al arrancar
    init_db()
    yield

app = FastAPI(title="Micro API", lifespan=lifespan)

# -----------------------
# Incluir Routers
# -----------------------
app.include_router(checkin.router)
app.include_router(evaluator.router)
app.include_router(auth_product.router)  # <--- Registrar el router de registro y productos

# ----------------------
# Root GET para Render / Swagger
# ----------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "API funcionando"}