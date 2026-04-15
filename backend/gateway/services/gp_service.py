from fastmcp import Client

from config import settings
from _common.schemas.gp_consultation import GPConsultation as GPConsultationSchema
from services.agent_result import AgentResult, to_response


async def fetch_gp_consultation(user_id: str, start_date: str) -> AgentResult:
    try:
        async with Client(settings.master_orchestrator_agent_url) as client:
            response = await client.call_tool(
                "run_gp_diagnosis",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
        raw_results = response.structured_content or {}
        consultation = raw_results.get("consultation", {})
        if not consultation:
            return to_response(error=f"No GP consultation found for user {user_id}")
        return to_response(data=GPConsultationSchema(**consultation))
    except Exception as exc:
        return to_response(error=str(exc))
