from fastmcp import Client

from config import settings
from schemas.diagnosis_schema import GPConsultationSchema
from services.exceptions import AgentConnectionError, NoDataFoundError


async def fetch_gp_consultation(user_id: str, start_date: str) -> GPConsultationSchema:
    try:
        async with Client(settings.gp_synthesis_agent_url) as client:
            result = await client.call_tool(
                "get_final_gp_consultation",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"gp_synthesis_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    data = payload.get("result", {})

    if not data:
        raise NoDataFoundError(f"No GP consultation found for user {user_id}")

    return GPConsultationSchema(**data)
