from fastmcp import Client

from config import settings
from schemas.consilium_schema import SpecialistFindingSchema
from services.exceptions import AgentConnectionError, NoDataFoundError


async def fetch_consilium(user_id: str, start_date: str) -> list[SpecialistFindingSchema]:
    try:
        async with Client(settings.consilium_agent_url) as client:
            result = await client.call_tool(
                "run_medical_consilium",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"consilium_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    findings = payload.get("result", [])

    if not findings:
        raise NoDataFoundError(f"No consilium findings for user {user_id}")

    return [SpecialistFindingSchema(**f) for f in findings]
