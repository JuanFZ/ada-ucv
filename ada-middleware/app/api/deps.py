import secrets
from fastapi import Header, HTTPException, status

from app.config import settings


def verify_service_token(x_ada_token: str = Header(default="")) -> None:
    """Verifica el token compartido entre Moodle y el Middleware."""
    if not x_ada_token or not secrets.compare_digest(x_ada_token, settings.ada_service_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de servicio inválido o ausente.",
        )

