from app.providers.openai_compatible import OpenAICompatibleAdapter


class OpenRouterAdapter(OpenAICompatibleAdapter):
    """Adaptador para OpenRouter API (modelos :free, compatible con OpenAI)."""

    name = "openrouter"
    ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

