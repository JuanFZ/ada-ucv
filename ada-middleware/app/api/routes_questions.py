import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.agent.orchestrator import QuestionOrchestrator
from app.api.deps import verify_service_token
from app.providers.base import ProviderError
from app.schemas.questions import QuestionGenerationRequest, QuestionGenerationResponse
from app.validators.question_validator import QuestionValidationError

logger = logging.getLogger("ada.middleware")
router = APIRouter(prefix="/v1/questions", tags=["questions"])


@router.post(
    "/generate",
    response_model=QuestionGenerationResponse,
    dependencies=[Depends(verify_service_token)],
)
async def generate_questions(payload: QuestionGenerationRequest) -> QuestionGenerationResponse:
    """Genera preguntas de opción múltiple validadas y exportadas a Moodle XML/GIFT."""
    orchestrator = QuestionOrchestrator()
    try:
        return await orchestrator.generate_multichoice_xml(payload)
    except QuestionValidationError as exc:
        logger.warning("Validación fallida: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se pudieron validar las preguntas generadas. Intenta reformular el tema o reducir la cantidad.",
        ) from exc
    except ProviderError as exc:
        logger.warning("Error de proveedor LLM: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="El servicio de IA no está disponible temporalmente o alcanzó su cuota. Inténtalo de nuevo en unos momentos.",
        ) from exc

