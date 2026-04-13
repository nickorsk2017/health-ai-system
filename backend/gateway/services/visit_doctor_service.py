from fastmcp import Client

from config import settings
from schemas.visit_schema import CreateVisitSchema, RecordVisitResponseSchema, VisitRecordSchema
from services.exceptions import AgentConnectionError, NoDataFoundError


async def record_visit(visit: CreateVisitSchema) -> RecordVisitResponseSchema:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
                "add_visit_doctor",
                {
                    "data": {
                        "user_id": visit.user_id,
                        "doctor_type": visit.doctor_type.value,
                        "visit_at": visit.visit_at,
                        "subjective": visit.subjective,
                        "objective": visit.objective,
                        "assessment": visit.assessment,
                        "plan": visit.plan,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    data = payload.get("result", {})

    if not data:
        raise NoDataFoundError("visit_doctor_agent returned empty result")

    return RecordVisitResponseSchema(success=data.get("success", False), visit_id=data.get("visit_id", ""))


async def fetch_visit_history(user_id: str, last_date_visit: str) -> list[VisitRecordSchema]:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
                "get_doctor_visits_history",
                {"data": {"user_id": user_id, "last_date_visit": last_date_visit, "doctor_type": ""}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    records = payload.get("result", [])

    if not records:
        raise NoDataFoundError(f"No visit history found for user {user_id}")

    return [VisitRecordSchema(**r) for r in records]
