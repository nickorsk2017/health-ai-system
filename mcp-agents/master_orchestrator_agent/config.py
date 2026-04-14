from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_history_agent_url: str
    labs_agent_url: str
    doctors_agent_url: str
    gp_synthesis_agent_url: str
    device_orchestrator_agent_url: str
    complaint_manager_agent_url: str

    mcp_port: int = 6350
    mcp_host: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
