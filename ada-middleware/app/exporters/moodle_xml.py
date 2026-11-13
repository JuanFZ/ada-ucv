from html import escape
from app.schemas.questions import MultipleChoiceQuestion


def _cdata(html_text: str) -> str:
    """Envuelve contenido en CDATA escapando cualquier secuencia ']]>' interna."""
    safe = html_text.replace("]]>", "]]]]><![CDATA[>")
    return f"<![CDATA[{safe}]]>"


def _wrap_paragraph(text: str) -> str:
    """Convierte texto plano en HTML limpio si no contiene etiquetas de párrafo."""
    stripped = text.strip()
    if not stripped:
        return ""
    if stripped.startswith("<p>") or stripped.startswith("<div>"):
        return stripped
    return f"<p>{escape(stripped)}</p>"


def export_multichoice_to_moodle_xml(questions: list[MultipleChoiceQuestion]) -> str:
    """Serializa de forma determinista preguntas de opción múltiple a formato Moodle XML."""
    lines: list[str] = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]

    for q in questions:
        shuffle = "true" if q.shuffle_answers else "false"
        lines.extend([
            '  <question type="multichoice">',
            "    <name>",
            f"      <text>{escape(q.name.strip())}</text>",
            "    </name>",
            '    <questiontext format="html">',
            f"      <text>{_cdata(_wrap_paragraph(q.question_text))}</text>",
            "    </questiontext>",
            '    <generalfeedback format="html">',
            f"      <text>{_cdata(_wrap_paragraph(q.general_feedback))}</text>",
            "    </generalfeedback>",
            "    <defaultgrade>1.0000000</defaultgrade>",
            "    <penalty>0.3333333</penalty>",
            "    <hidden>0</hidden>",
            "    <single>true</single>",
            f"    <shuffleanswers>{shuffle}</shuffleanswers>",
            "    <answernumbering>abc</answernumbering>",
        ])

        for opt in q.options:
            lines.extend([
                f'    <answer fraction="{opt.fraction}" format="html">',
                f"      <text>{_cdata(_wrap_paragraph(opt.text))}</text>",
                '      <feedback format="html">',
                f"        <text>{_cdata(_wrap_paragraph(opt.feedback))}</text>",
                "      </feedback>",
                "    </answer>",
            ])

        lines.append("  </question>")

    lines.append("</quiz>")
    return "\n".join(lines) + "\n"

