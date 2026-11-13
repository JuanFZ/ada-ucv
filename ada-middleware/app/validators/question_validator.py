from app.schemas.questions import GeneratedQuestionBatch


class QuestionValidationError(ValueError):
    """Error determinista cuando el lote generado incumple reglas de Moodle."""


def validate_question_batch(batch: GeneratedQuestionBatch, expected_count: int) -> None:
    """Valida reglas estructurales y pedagógicas antes de exportar a Moodle XML."""
    if len(batch.questions) != expected_count:
        raise QuestionValidationError(
            f"Se solicitaron {expected_count} preguntas, pero el modelo devolvió {len(batch.questions)}."
        )

    for idx, q in enumerate(batch.questions, start=1):
        if not q.name.strip():
            raise QuestionValidationError(f"Pregunta {idx}: el título 'name' está vacío.")
        if not q.question_text.strip():
            raise QuestionValidationError(f"Pregunta {idx}: el enunciado 'question_text' está vacío.")

        normalized_options = [opt.text.strip().lower() for opt in q.options]
        if any(not text for text in normalized_options):
            raise QuestionValidationError(f"Pregunta {idx}: contiene una opción con texto vacío.")
        if len(set(normalized_options)) != len(normalized_options):
            raise QuestionValidationError(f"Pregunta {idx}: contiene opciones de respuesta duplicadas.")

        correct = [opt for opt in q.options if opt.fraction == 100]
        incorrect = [opt for opt in q.options if opt.fraction == 0]
        if len(correct) != 1:
            raise QuestionValidationError(
                f"Pregunta {idx}: debe tener exactamente 1 opción correcta con fraction=100 (tiene {len(correct)})."
            )
        if len(correct) + len(incorrect) != len(q.options):
            raise QuestionValidationError(
                f"Pregunta {idx}: en respuesta única las opciones deben tener fraction 100 o 0."
            )

