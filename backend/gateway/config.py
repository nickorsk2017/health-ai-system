from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    visit_doctor_agent_url: str
    consilium_agent_url: str
    gp_synthesis_agent_url: str
    user_service_url: str

    cors_origins: list[str] = ["http://localhost:3000"]

    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
