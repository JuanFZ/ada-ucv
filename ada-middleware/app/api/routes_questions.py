from fastapi import APIRouter, Depends, HTTPException, status

from app.agent.orchestrator import QuestionOrchestrator
from app.api.deps import verify_service_token
from app.providers.base import ProviderError
from app.schemas.questions import QuestionGenerationRequest, QuestionGenerationResponse
from app.validators.question_validator import QuestionValidationError

router = APIRouter(prefix="/v1/questions", tags=["questions"])


@router.post(
    "/generate",
    response_model=QuestionGenerationResponse,
    dependencies=[Depends(verify_service_token)],
)
async def generate_questions(payload: QuestionGenerationRequest) -> QuestionGenerationResponse:
    """Genera preguntas de opción múltiple validadas y exportadas a Moodle XML."""
    orchestrator = QuestionOrchestrator()
    try:
        return await orchestrator.generate_multichoice_xml(payload)
    except QuestionValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except ProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

