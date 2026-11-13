from fastapi import APIRouter

from app.config import settings
from app.providers.router import ProviderRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    """Endpoint de verificación operativa del Middleware."""
    provider_router = ProviderRouter()
    return {
        "status": "ok",
        "primary_provider": settings.ada_primary_provider,
        "fallback_provider": settings.ada_fallback_provider,
        "configured_providers": provider_router.configured_providers(),
    }

