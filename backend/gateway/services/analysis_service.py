from datetime import datetime, timezone

from fastmcp import Client

from config import settings
from schemas.analysis_schema import (
    AnalysisByPromptRequestSchema,
    AnalysisByPromptResponseSchema,
    AnalysisRecordSchema,
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    MutateAnalysisResponseSchema,
    UpdateAnalysisSchema,
)
from services.agent_result import AgentResult, to_response


async def record_analysis(data: AnalysisRequestSchema) -> AgentResult:
    analysis_date = data.analysis_date
    if analysis_date.tzinfo is None:
        analysis_date = analysis_date.replace(tzinfo=timezone.utc)
    else:
        analysis_date = analysis_date.astimezone(timezone.utc)
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "add_patient_analysis",
                {
                    "data": {
                        "user_id": data.user_id,
                        "analysis_text": data.analysis_text,
                        "analysis_date": analysis_date.isoformat(),
                    }
                },
            )
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        return to_response(data=AnalysisResponseSchema(success=analysis_data.get("success", False)))
    except Exception as exc:
        return to_response(error=str(exc))


async def fetch_analyses(user_id: str, start_date: datetime) -> AgentResult:
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    else:
        start_date = start_date.astimezone(timezone.utc)
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "get_patient_analyses",
                {"data": {"user_id": user_id, "start_date": start_date.isoformat()}},
            )
        raw_results = response.structured_content or {}
        analyses_collection = raw_results.get("result", [])
        return to_response(data=[AnalysisRecordSchema(**a) for a in analyses_collection])
    except Exception as exc:
        return to_response(error=str(exc))


async def update_analysis(analysis_id: str, data: UpdateAnalysisSchema) -> AgentResult:
    analysis_date = data.analysis_date
    if analysis_date is not None:
        if analysis_date.tzinfo is None:
            analysis_date = analysis_date.replace(tzinfo=timezone.utc)
        else:
            analysis_date = analysis_date.astimezone(timezone.utc)
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "update_analysis",
                {
                    "data": {
                        "analysis_id": analysis_id,
                        "analysis_text": data.analysis_text,
                        "analysis_date": analysis_date.isoformat() if analysis_date else None,
                    }
                },
            )
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        if not analysis_data.get("success"):
            return to_response(error=analysis_data.get("error", f"Analysis {analysis_id} not found"))
        return to_response(data=MutateAnalysisResponseSchema(success=True))
    except Exception as exc:
        return to_response(error=str(exc))


async def delete_analysis(analysis_id: str) -> AgentResult:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "delete_analysis",
                {"data": {"analysis_id": analysis_id}},
            )
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        if not analysis_data.get("success"):
            return to_response(error=analysis_data.get("error", f"Analysis {analysis_id} not found"))
        return to_response(data=MutateAnalysisResponseSchema(success=True))
    except Exception as exc:
        return to_response(error=str(exc))


async def create_analyses_from_prompt(data: AnalysisByPromptRequestSchema) -> AgentResult:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "create_analyses_from_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        return to_response(data=AnalysisByPromptResponseSchema(
            success=analysis_data.get("success", False),
            list_missing_analysis=analysis_data.get("list_missing_analysis", []),
        ))
    except Exception as exc:
        return to_response(error=str(exc))
