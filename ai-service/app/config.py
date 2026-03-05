from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Service"
    app_version: str = "1.0.0"
    environment: str = "production"
    debug: bool = False
    log_level: str = "INFO"
    cors_origins: list[str] = ["*"]

    # Optional external model config (API still works without these)
    llama3_api_url: str = "https://fastchat.ideeza.com/v1/chat/completions"
    llama3_model: str = "llama-3-70b-instruct"
    llama3_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
