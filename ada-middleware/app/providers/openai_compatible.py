import json
import time
from typing import Any
import httpx

from app.providers.base import (
    LLMProvider,
    ProviderAuthError,
    ProviderError,
    ProviderRateLimitError,
    ProviderResult,
)


class OpenAICompatibleAdapter(LLMProvider):
    """Base reutilizable para APIs compatibles con OpenAI Chat Completions (Mistral, Groq, etc.)."""

    ENDPOINT: str = ""

    def __init__(self, api_key: str, model: str, timeout: float = 30.0) -> None:
        self._api_key = api_key.strip()
        self._model = model.strip()
        self._timeout = timeout

    def is_configured(self) -> bool:
        return bool(self._api_key)

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any],
    ) -> ProviderResult:
        if not self.is_configured():
            raise ProviderAuthError(f"{self.name.upper()}_API_KEY no está configurada.")

        schema_hint = json.dumps(json_schema, ensure_ascii=False)
        full_system = (
            f"{system_prompt}\n\n"
            "Responde ÚNICAMENTE con un objeto JSON válido que cumpla exactamente este JSON Schema:\n"
            f"{schema_hint}"
        )

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": full_system},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.4,
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(self.ENDPOINT, json=payload, headers=headers)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Error de red con {self.name}: {exc}") from exc

        latency_ms = int((time.perf_counter() - start) * 1000)

        if resp.status_code == 429:
            raise ProviderRateLimitError(f"{self.name} alcanzó el límite de cuota/tasa (HTTP 429).")
        if resp.status_code in (401, 403):
            raise ProviderAuthError(
                f"Error de autenticación o acceso en {self.name} (HTTP {resp.status_code})."
            )
        if resp.status_code >= 400:
            raise ProviderError(f"{self.name} devolvió HTTP {resp.status_code}: {resp.text[:300]}")

        data = resp.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"Respuesta inesperada de {self.name}: {data}") from exc

        return ProviderResult(
            provider=self.name,
            model=self._model,
            raw_json=content,
            latency_ms=latency_ms,
        )

