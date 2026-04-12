from fastmcp import FastMCP

from config import settings
from tools.get_daily_oura_biometrics import get_daily_oura_biometrics as _get_daily_oura_biometrics

mcp = FastMCP("oura-ring-mcp-agent")


@mcp.resource("config://settings")
def get_config() -> str:
    return f"openai_model: {settings.openai_model}"


@mcp.tool(name="get_daily_oura_biometrics")
async def get_daily_oura_biometrics(date: str, user_id: str) -> list[dict]:
    """Return synthetic Oura Ring daily biometrics from a start date to today.

    Args:
        date: ISO 8601 start date (YYYY-MM-DD).
        user_id: Identifier of the user whose data is requested.
    """
    
    records = await _get_daily_oura_biometrics(date, user_id)
    return [r.model_dump() for r in records]


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()