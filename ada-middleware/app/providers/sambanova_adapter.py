from app.providers.openai_compatible import OpenAICompatibleAdapter


class SambaNovaAdapter(OpenAICompatibleAdapter):
    """Adaptador para SambaNova Cloud API (compatible con OpenAI)."""

    name = "sambanova"
    ENDPOINT = "https://api.sambanova.ai/v1/chat/completions"

