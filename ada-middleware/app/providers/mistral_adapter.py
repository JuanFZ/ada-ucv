from app.providers.openai_compatible import OpenAICompatibleAdapter


class MistralAdapter(OpenAICompatibleAdapter):
    """Adaptador para Mistral AI (La Plateforme, UE)."""

    name = "mistral"
    ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
