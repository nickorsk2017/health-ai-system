from datetime import timezone

from fastmcp import Client

from config import settings
from schemas.complaint_schema import ComplaintRecordSchema, ComplaintsByPromptRequestSchema, UpsertComplaintSchema
from services.agent_result import AgentResult, to_response


async def upsert_complaint(complaint_id: str | None, data: UpsertComplaintSchema) -> AgentResult:
    date_public = data.date_public
    if date_public.tzinfo is None:
        date_public = date_public.replace(tzinfo=timezone.utc)
    else:
        date_public = date_public.astimezone(timezone.utc)
    try:
        payload: dict = {
            "user_id": data.user_id,
            "problem_health": data.problem_health,
            "date_public": date_public.isoformat(),
        }
        if complaint_id:
            payload["complaint_id"] = complaint_id

        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool("upsert_complaint", {"data": payload})

        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return to_response(error="complaint_manager_agent returned failure on upsert_complaint")
        return to_response()
    except Exception as exc:
        return to_response(error=str(exc))


async def fetch_complaints(user_id: str) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "get_complaints",
                {"data": {"user_id": user_id}},
            )
        response_content = response.structured_content
        complaints_collection = (
            response_content.get("result") if isinstance(response_content, dict) else None
        )
        return to_response(data=[ComplaintRecordSchema(**c) for c in complaints_collection])
    except Exception as exc:
        return to_response(error=str(exc))


async def create_complaints_from_prompt(data: ComplaintsByPromptRequestSchema) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "create_complaints_by_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
        response_content = response.structured_content
        complaints_collection = (
            response_content.get("result") if isinstance(response_content, dict) else None
        )
        return to_response(data=[ComplaintRecordSchema(**c) for c in complaints_collection])
    except Exception as exc:
        return to_response(error=str(exc))


async def mark_complaint_read(complaint_id: str) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "mark_as_read",
                {"data": {"complaint_id": complaint_id}},
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return to_response(error=raw_results.get("error", f"Complaint {complaint_id} not found"))
        return to_response()
    except Exception as exc:
        return to_response(error=str(exc))


async def remove_complaint(complaint_id: str) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "delete_complaint",
                {"data": {"complaint_id": complaint_id}},
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return to_response(error=raw_results.get("error", f"Complaint {complaint_id} not found"))
        return to_response()
    except Exception as exc:
        return to_response(error=str(exc))
