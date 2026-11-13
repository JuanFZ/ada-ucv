from app.providers.openai_compatible import OpenAICompatibleAdapter


class GroqAdapter(OpenAICompatibleAdapter):
    """Adaptador para Groq API."""

    name = "groq"
    ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
