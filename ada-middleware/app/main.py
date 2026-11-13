from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_questions import router as questions_router

app = FastAPI(
    title="ADA Middleware",
    description="Servicio desacoplado de inferencia, validación y exportación para el Agente ADA (UCV).",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(questions_router)

