from fastmcp import Client

from config import settings
from schemas.consilium_schema import SpecialistFindingSchema
from services.agent_result import AgentResult, to_response


async def fetch_consilium(user_id: str, start_date: str) -> AgentResult:
    try:
        async with Client(settings.doctors_agent_url) as client:
            response = await client.call_tool(
                "run_medical_consilium",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
        raw_results = response.structured_content or {}
        findings_collection = raw_results.get("result", [])
        if not findings_collection:
            return to_response(error=f"No consilium findings for user {user_id}")
        return to_response(data=[SpecialistFindingSchema(**f) for f in findings_collection])
    except Exception as exc:
        return to_response(error=str(exc))
