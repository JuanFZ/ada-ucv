from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class ProviderError(RuntimeError):
    """Error base de comunicación con un proveedor de LLM."""


class ProviderRateLimitError(ProviderError):
    """Cuota o límite de tasa excedido (HTTP 429)."""


class ProviderAuthError(ProviderError):
    """Credencial ausente o inválida (HTTP 401/403)."""


@dataclass(frozen=True)
class ProviderResult:
    """Resultado crudo normalizado devuelto por un adaptador de LLM."""

    provider: str
    model: str
    raw_json: str
    latency_ms: int


class LLMProvider(ABC):
    """Puerto abstracto para desacoplar ADA de proveedores comerciales específicos."""

    name: str

    @abstractmethod
    def is_configured(self) -> bool:
        """Indica si el proveedor tiene API key configurada."""

    @abstractmethod
    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any],
    ) -> ProviderResult:
        """Ejecuta inferencia y retorna una cadena JSON ajustada al esquema."""

