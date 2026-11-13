from datetime import datetime, timezone
import json
from pydantic import ValidationError

from app.config import settings
from app.exporters.gift import export_multichoice_to_gift
from app.exporters.moodle_xml import export_multichoice_to_moodle_xml
from app.providers.router import ProviderRouter
from app.schemas.questions import (
    GeneratedQuestionBatch,
    QuestionGenerationRequest,
    QuestionGenerationResponse,
)
from app.validators.question_validator import QuestionValidationError, validate_question_batch

SYSTEM_PROMPT_QUESTIONS = """Eres ADA, un asistente tecnopedagógico para docentes universitarios de la Facultad de Ciencias de la UCV.
Tu tarea es generar preguntas de opción múltiple (respuesta única) rigurosas, claras y bien redactadas en español académico.

Reglas obligatorias:
1. Genera exactamente la cantidad de preguntas solicitada.
2. Cada pregunta debe tener 4 opciones de respuesta plausibles.
3. Exactamente UNA opción debe tener fraction=100 (la correcta) y las otras tres deben tener fraction=0.
4. Incluye retroalimentación breve y pedagógica en cada opción y en general_feedback.
5. No incluyas numeración tipo "a)", "b)" dentro del texto de las opciones (Moodle las numera automáticamente).
"""


def _extract_json_text(raw: str) -> str:
    """Limpia bloques markdown ```json ... ``` si un modelo los incluye alrededor del JSON."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


class QuestionOrchestrator:
    """Orquesta generación -> validación -> reparación acotada -> exportación determinista."""

    def __init__(self, router: ProviderRouter | None = None) -> None:
        self._router = router or ProviderRouter()

    async def generate_multichoice_xml(
        self, req: QuestionGenerationRequest
    ) -> QuestionGenerationResponse:
        schema = GeneratedQuestionBatch.model_json_schema()
        base_user_prompt = (
            f"Idioma: {req.language}\n"
            f"Contexto Moodle: versión {req.moodle_version}, curso '{req.course_shortname or 'General'}'\n"
            f"Nivel de dificultad: {req.difficulty}\n"
            f"Cantidad exacta de preguntas: {req.count}\n"
            f"Tema o contenido base:\n{req.topic}\n"
        )

        last_error = ""
        total_latency = 0
        retries = 0
        user_prompt = base_user_prompt

        for attempt in range(settings.ada_max_retries + 1):
            result = await self._router.generate_json(
                system_prompt=SYSTEM_PROMPT_QUESTIONS,
                user_prompt=user_prompt,
                json_schema=schema,
                requested_provider=req.provider,
            )
            total_latency += result.latency_ms

            try:
                raw_obj = json.loads(_extract_json_text(result.raw_json))
                batch = GeneratedQuestionBatch.model_validate(raw_obj)
                validate_question_batch(batch, expected_count=req.count)
                stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                if req.export_format == "gift":
                    exported_output = export_multichoice_to_gift(batch.questions)
                    filename = f"ada_preguntas_{stamp}.gift.txt"
                else:
                    exported_output = export_multichoice_to_moodle_xml(batch.questions)
                    filename = f"ada_preguntas_{stamp}.xml"
                return QuestionGenerationResponse(
                    provider_used=result.provider,
                    model_used=result.model,
                    latency_ms=total_latency,
                    retries=retries,
                    questions=batch.questions,
                    exported_content=exported_output,
                    filename=filename,
                )
            except (json.JSONDecodeError, ValidationError, QuestionValidationError) as exc:
                last_error = str(exc)
                retries += 1
                user_prompt = (
                    f"{base_user_prompt}\n"
                    f"CORRECCIÓN REQUERIDA (intento previo inválido): {last_error}\n"
                    "Corrige estrictamente el JSON para cumplir todas las reglas."
                )

        raise QuestionValidationError(
            f"No se pudo generar un lote válido tras {settings.ada_max_retries + 1} intentos: {last_error}"
        )

