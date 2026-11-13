import xml.etree.ElementTree as ET
import pytest

from app.agent.orchestrator import _extract_json_text
from app.exporters.gift import export_multichoice_to_gift
from app.exporters.moodle_xml import export_multichoice_to_moodle_xml
from app.schemas.questions import GeneratedQuestionBatch, MultipleChoiceQuestion, QuestionOption
from app.validators.question_validator import QuestionValidationError, validate_question_batch


def _sample_batch() -> GeneratedQuestionBatch:
    return GeneratedQuestionBatch(
        questions=[
            MultipleChoiceQuestion(
                name="Complejidad búsqueda binaria",
                question_text="¿Cuál es la complejidad temporal promedio de búsqueda en un árbol binario balanceado?",
                options=[
                    QuestionOption(text="O(log n)", fraction=100, feedback="Correcto."),
                    QuestionOption(text="O(n^2)", fraction=0, feedback="Incorrecto."),
                    QuestionOption(text="O(1)", fraction=0, feedback="Incorrecto."),
                    QuestionOption(text="O(n log n)", fraction=0, feedback="Incorrecto."),
                ],
                general_feedback="En árboles balanceados la altura es O(log n).",
            )
        ]
    )


def test_validator_accepts_valid_batch() -> None:
    batch = _sample_batch()
    validate_question_batch(batch, expected_count=1)


def test_validator_rejects_duplicate_options() -> None:
    batch = _sample_batch()
    batch.questions[0].options[1].text = "O(log n)"
    with pytest.raises(QuestionValidationError, match="duplicadas"):
        validate_question_batch(batch, expected_count=1)


def test_validator_rejects_multiple_correct_answers() -> None:
    batch = _sample_batch()
    batch.questions[0].options[1].fraction = 100
    with pytest.raises(QuestionValidationError, match="exactamente 1 opción correcta"):
        validate_question_batch(batch, expected_count=1)


def test_moodle_xml_export_is_valid_xml_with_special_chars() -> None:
    batch = _sample_batch()
    batch.questions[0].question_text = "Si x < 5 & y > 2 ]]> ¿qué ocurre con áéíóúñ?"
    xml_str = export_multichoice_to_moodle_xml(batch.questions)

    root = ET.fromstring(xml_str)
    assert root.tag == "quiz"
    questions = root.findall("question")
    assert len(questions) == 1
    assert questions[0].attrib["type"] == "multichoice"
    assert "áéíóúñ" in xml_str


def test_gift_export_escapes_reserved_chars_and_includes_feedback() -> None:
    batch = _sample_batch()
    batch.questions[0].question_text = "¿Qué significa f(x) = {a: b} ~ #1?"
    gift_str = export_multichoice_to_gift(batch.questions)

    assert "::Complejidad búsqueda binaria::" in gift_str
    assert r"\= \{a\: b\} \~ \#1?" in gift_str
    assert "=O(log n) #Correcto." in gift_str
    assert "~O(n^2) #Incorrecto." in gift_str
    assert "####En árboles balanceados" in gift_str


def test_extract_json_text_strips_markdown_fences() -> None:
    raw = 'Aquí tienes:\n```json\n{"questions": []}\n```\n'
    assert _extract_json_text(raw) == '{"questions": []}'

