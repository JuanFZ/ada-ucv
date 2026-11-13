from typing import Any

from app.config import settings
from app.providers.base import LLMProvider, ProviderError, ProviderRateLimitError, ProviderResult
from app.providers.gemini_adapter import GeminiAdapter
from app.providers.groq_adapter import GroqAdapter
from app.providers.mistral_adapter import MistralAdapter
from app.providers.sambanova_adapter import SambaNovaAdapter


class ProviderRouter:
    """Enruta inferencias al proveedor primario y conmuta al fallback si hay cuota agotada o fallo."""

    def __init__(self) -> None:
        self._providers: dict[str, LLMProvider] = {
            "sambanova": SambaNovaAdapter(
                api_key=settings.sambanova_api_key,
                model=settings.sambanova_model,
                timeout=settings.ada_timeout_seconds,
            ),
            "gemini": GeminiAdapter(
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
                timeout=settings.ada_timeout_seconds,
            ),
            "mistral": MistralAdapter(
                api_key=settings.mistral_api_key,
                model=settings.mistral_model,
                timeout=settings.ada_timeout_seconds,
            ),
            "groq": GroqAdapter(
                api_key=settings.groq_api_key,
                model=settings.groq_model,
                timeout=settings.ada_timeout_seconds,
            ),
        }

    def configured_providers(self) -> list[str]:
        return [name for name, prov in self._providers.items() if prov.is_configured()]

    def _resolve_order(self, requested: str) -> list[LLMProvider]:
        if requested != "auto":
            prov = self._providers.get(requested)
            if not prov:
                raise ProviderError(f"Proveedor desconocido: {requested}")
            return [prov]

        order: list[LLMProvider] = []
        for name in (settings.ada_primary_provider, settings.ada_fallback_provider):
            prov = self._providers.get(name)
            if prov and prov.is_configured() and prov not in order:
                order.append(prov)
        return order

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any],
        requested_provider: str = "auto",
    ) -> ProviderResult:
        candidates = self._resolve_order(requested_provider)
        if not candidates:
            raise ProviderError(
                "No hay proveedores de IA configurados. Define GROQ_API_KEY o GEMINI_API_KEY en .env."
            )

        errors: list[str] = []
        for provider in candidates:
            try:
                return await provider.generate_json(system_prompt, user_prompt, json_schema)
            except (ProviderRateLimitError, ProviderError) as exc:
                errors.append(f"{provider.name}: {exc}")
                continue

        raise ProviderError("Todos los proveedores fallaron: " + " | ".join(errors))

