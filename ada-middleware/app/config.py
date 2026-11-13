from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del Middleware ADA cargada desde variables de entorno."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ada_service_token: str = "dev-ada-token"
    ada_primary_provider: str = "groq"
    ada_fallback_provider: str = "gemini"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    ada_timeout_seconds: float = 30.0
    ada_max_retries: int = 1


settings = Settings()

