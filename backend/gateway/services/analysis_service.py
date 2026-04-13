from fastmcp import Client

from config import settings
from schemas.analysis_schema import AnalysisRecordSchema, AnalysisRequestSchema, AnalysisResponseSchema
from services.exceptions import AgentConnectionError, NoDataFoundError


async def record_analysis(data: AnalysisRequestSchema) -> AnalysisResponseSchema:
    try:
        async with Client(settings.analysis_agent_url) as client:
            result = await client.call_tool(
                "add_patient_analysis",
                {
                    "data": {
                        "user_id": data.user_id,
                        "analysis": data.analysis,
                        "date": data.date.isoformat(),
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"patient_analysis_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    response_data = payload.get("result", {})

    if not response_data:
        raise AgentConnectionError("patient_analysis_agent returned empty result")

    return AnalysisResponseSchema(success=response_data.get("success", False))


async def fetch_analyses(user_id: str, start_date: str) -> list[AnalysisRecordSchema]:
    try:
        async with Client(settings.analysis_agent_url) as client:
            result = await client.call_tool(
                "get_patient_analyses",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"patient_analysis_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    records = payload.get("result", [])

    if not records:
        raise NoDataFoundError(f"No analysis records found for user {user_id}")

    return [AnalysisRecordSchema(**r) for r in records]
