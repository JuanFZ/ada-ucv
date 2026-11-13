from typing import Literal
from pydantic import BaseModel, Field


class QuestionOption(BaseModel):
    """Opción individual de una pregunta de opción múltiple."""

    text: str = Field(..., min_length=1, description="Texto de la opción de respuesta.")
    fraction: int = Field(..., description="100 para la respuesta correcta, 0 para incorrectas.")
    feedback: str = Field(default="", description="Retroalimentación específica para esta opción.")


class MultipleChoiceQuestion(BaseModel):
    """Pregunta de opción múltiple (respuesta única) lista para exportar a Moodle."""

    name: str = Field(..., min_length=3, max_length=120, description="Título corto en el banco de preguntas.")
    question_text: str = Field(..., min_length=5, description="Enunciado de la pregunta.")
    options: list[QuestionOption] = Field(..., min_length=2, max_length=6)
    general_feedback: str = Field(default="", description="Retroalimentación general tras responder.")
    shuffle_answers: bool = Field(default=True)


class GeneratedQuestionBatch(BaseModel):
    """Contenedor raíz devuelto por el LLM."""

    questions: list[MultipleChoiceQuestion] = Field(..., min_length=1)


class QuestionGenerationRequest(BaseModel):
    """Solicitud enviada desde Moodle al Middleware."""

    moodle_version: Literal["4.5", "5.0"] = "5.0"
    course_shortname: str = Field(default="", max_length=100)
    topic: str = Field(..., min_length=3, max_length=500)
    question_type: Literal["multichoice"] = "multichoice"
    count: int = Field(default=3, ge=1, le=10)
    difficulty: Literal["basic", "intermediate", "advanced"] = "intermediate"
    language: str = Field(default="es", max_length=10)
    provider: Literal["auto", "mistral", "gemini", "groq"] = "auto"


class QuestionGenerationResponse(BaseModel):
    """Respuesta estructurada del Middleware hacia Moodle."""

    status: Literal["ok"] = "ok"
    provider_used: str
    model_used: str
    latency_ms: int
    retries: int
    questions: list[MultipleChoiceQuestion]
    exported_content: str
    filename: str

