from app.schemas.questions import MultipleChoiceQuestion


def _escape_gift(text: str) -> str:
    """Escapa caracteres reservados de la sintaxis GIFT de Moodle."""
    escaped = text.strip().replace("\\", "\\\\")
    for ch in ("~", "=", "#", "{", "}", ":"):
        escaped = escaped.replace(ch, f"\\{ch}")
    return escaped.replace("\n", "\\n")


def export_multichoice_to_gift(questions: list[MultipleChoiceQuestion]) -> str:
    """Serializa de forma determinista preguntas de opción múltiple a formato GIFT."""
    blocks: list[str] = []

    for q in questions:
        title = _escape_gift(q.name)
        stem = _escape_gift(q.question_text)
        lines = [f"::{title}:: {stem} {{"]

        for opt in q.options:
            prefix = "=" if opt.fraction == 100 else "~"
            opt_text = _escape_gift(opt.text)
            fb = _escape_gift(opt.feedback)
            if fb:
                lines.append(f"    {prefix}{opt_text} #{fb}")
            else:
                lines.append(f"    {prefix}{opt_text}")

        if q.general_feedback.strip():
            lines.append(f"    ####{_escape_gift(q.general_feedback)}")

        lines.append("}")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks) + "\n"

