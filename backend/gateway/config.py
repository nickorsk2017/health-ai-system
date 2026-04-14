from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_history_agent_url: str = "http://localhost:6332/mcp"
    doctors_agent_url: str = "http://localhost:6333/mcp"
    gp_synthesis_agent_url: str = "http://localhost:6334/mcp"
    labs_agent_url: str = "http://localhost:6444/mcp"
    user_service_url: str = "http://localhost:8001"
    device_orchestrator_agent_url: str = "http://localhost:6340/mcp"
    complaint_manager_agent_url: str = "http://localhost:6341/mcp"
    appointment_scheduler_agent_url: str = "http://localhost:6342/mcp"
    master_orchestrator_agent_url: str = "http://localhost:6350/mcp"

    cors_origins: list[str] = ["http://localhost:3000"]

    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
