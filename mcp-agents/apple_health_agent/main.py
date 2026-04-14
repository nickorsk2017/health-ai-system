from fastmcp import FastMCP

from config import settings
from tools.get_apple_health_metrics import get_apple_health_metrics as _get_apple_health_metrics

mcp = FastMCP("apple-health-mcp-agent")


@mcp.resource("config://settings")
def get_config() -> str:
    return f"openai_model: {settings.openai_model}"


@mcp.tool(name="get_apple_health_metrics")
async def get_apple_health_metrics(date: str, user_id: str, diagnosis_mock: str = "") -> list[dict]:
    """Return synthetic Apple HealthKit daily metrics from a start date to today.

    Args:
        date: ISO 8601 start date (YYYY-MM-DD).
        user_id: Identifier of the user whose data is requested.
        diagnosis_mock: Optional diagnosis name to simulate condition-specific biometrics
            (e.g. "Pheochromocytoma"). Leave empty for healthy baseline data.
    """
    records = await _get_apple_health_metrics(date, user_id, diagnosis_mock or None)
    return [r.model_dump() for r in records]


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)

def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
