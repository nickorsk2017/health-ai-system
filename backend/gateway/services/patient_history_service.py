from datetime import datetime, timezone

from fastmcp import Client

from config import settings
from schemas.patient_history_schema import (
    CreatePatientHistorySchema,
    HistoryFromPromptRequestSchema,
    HistoryFromPromptResponseSchema,
    MutatePatientHistoryResponseSchema,
    PatientHistoryRecordSchema,
    RecordPatientHistoryResponseSchema,
    UpdatePatientHistorySchema,
)
from services.agent_result import AgentResult, to_response


async def record_patient_history(data: CreatePatientHistorySchema) -> AgentResult:
    history_date = data.history_date
    if history_date.tzinfo is None:
        history_date = history_date.replace(tzinfo=timezone.utc)
    else:
        history_date = history_date.astimezone(timezone.utc)
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "add_patient_history",
                {
                    "data": {
                        "user_id": data.user_id,
                        "doctor_type": data.doctor_type.value,
                        "history_date": history_date.isoformat(),
                        "subjective": data.subjective,
                        "objective": data.objective,
                        "assessment": data.assessment,
                        "plan": data.plan,
                    }
                },
            )
        raw_results = response.structured_content
        if not raw_results.get("success"):
            return to_response(error="client_history_agent returned failure on add_patient_history")
        return to_response(data=RecordPatientHistoryResponseSchema(
            success=True,
            history_id=raw_results.get("history_id", ""),
        ))
    except Exception as exc:
        return to_response(error=str(exc))


async def fetch_patient_history(user_id: str, last_history_date: datetime) -> AgentResult:
    if last_history_date.tzinfo is None:
        last_history_date = last_history_date.replace(tzinfo=timezone.utc)
    else:
        last_history_date = last_history_date.astimezone(timezone.utc)
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "get_patient_history",
                {"data": {"user_id": user_id, "last_history_date": last_history_date.isoformat(), "doctor_type": ""}},
            )
        raw_results = response.structured_content or {}
        history_collection = raw_results.get("result", [])
        return to_response(data=[PatientHistoryRecordSchema(**r) for r in history_collection])
    except Exception as exc:
        return to_response(error=str(exc))


async def create_history_from_prompt(data: HistoryFromPromptRequestSchema) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "create_history_from_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
        raw_results = response.structured_content or {}
        history_data = raw_results.get("result", raw_results)
        return to_response(data=HistoryFromPromptResponseSchema(
            success=history_data.get("success", False),
            count=history_data.get("count", 0),
        ))
    except Exception as exc:
        return to_response(error=str(exc))


async def update_patient_history(history_id: str, data: UpdatePatientHistorySchema) -> AgentResult:
    history_date = data.history_date
    if history_date.tzinfo is None:
        history_date = history_date.replace(tzinfo=timezone.utc)
    else:
        history_date = history_date.astimezone(timezone.utc)
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "update_patient_history",
                {
                    "data": {
                        "history_id": history_id,
                        "history_date": history_date.isoformat(),
                        "subjective": data.subjective,
                        "objective": data.objective,
                        "assessment": data.assessment,
                        "plan": data.plan,
                    }
                },
            )
        raw_results = response.structured_content or {}
        history_data = raw_results.get("result", raw_results)
        if not history_data.get("success"):
            return to_response(error=history_data.get("error", f"Patient history record {history_id} not found"))
        return to_response(data=MutatePatientHistoryResponseSchema(success=True))
    except Exception as exc:
        return to_response(error=str(exc))


async def delete_patient_history(history_id: str) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "delete_patient_history",
                {"data": {"history_id": history_id}},
            )
        raw_results = response.structured_content or {}
        history_data = raw_results.get("result", raw_results)
        if not history_data.get("success"):
            return to_response(error=history_data.get("error", f"Patient history record {history_id} not found"))
        return to_response(data=MutatePatientHistoryResponseSchema(success=True))
    except Exception as exc:
        return to_response(error=str(exc))
