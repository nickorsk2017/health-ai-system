from datetime import datetime, timezone

from fastmcp import Client

from config import settings
from _common.schemas.specialist_finding import SpecialistFinding as SpecialistFindingSchema
from services.agent_result import AgentResult, to_response


async def fetch_consilium(user_id: str, start_date: datetime) -> AgentResult:
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    else:
        start_date = start_date.astimezone(timezone.utc)
    try:
        async with Client(settings.master_orchestrator_agent_url) as client:
            response = await client.call_tool(
                "run_comprehensive_evaluation",
                {"data": {"user_id": user_id, "start_date": start_date.isoformat()}},
            )
        raw_results = response.structured_content or {}
        findings_collection = raw_results.get("findings", [])
        if not findings_collection:
            return to_response(error=f"No consilium findings for user {user_id}")
        return to_response(data=[SpecialistFindingSchema(**f) for f in findings_collection])
    except Exception as exc:
        return to_response(error=str(exc))
