from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del Middleware ADA cargada desde variables de entorno."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ada_service_token: str = "dev-ada-token"
    ada_primary_provider: str = "mistral"
    ada_fallback_provider: str = "gemini"

    mistral_api_key: str = ""
    mistral_model: str = "mistral-small-latest"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"

    sambanova_api_key: str = ""
    sambanova_model: str = "Meta-Llama-3.3-70B-Instruct"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    ada_timeout_seconds: float = 30.0
    ada_max_retries: int = 1


settings = Settings()

