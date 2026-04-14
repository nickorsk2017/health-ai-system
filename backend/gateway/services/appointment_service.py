from fastmcp import Client

from config import settings
from schemas.appointment_schema import AppointmentRecordSchema, CreateAppointmentSchema
from services.exceptions import AgentConnectionError


async def create_appointment(data: CreateAppointmentSchema) -> AppointmentRecordSchema:
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            result = await client.call_tool(
                "create_appointment",
                {
                    "data": {
                        "complaint_id": data.complaint_id,
                        "appointment_date": data.appointment_date,
                        "doctor_type": data.doctor_type,
                        "problem_notes": data.problem_notes,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"appointment_scheduler_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    if not payload.get("success"):
        raise AgentConnectionError(
            payload.get("error", "appointment_scheduler_agent returned failure")
        )

    records = await fetch_appointments("")
    match = next((r for r in records if r.appointment_id == payload["appointment_id"]), None)
    if not match:
        raise AgentConnectionError("Appointment created but could not be retrieved")
    return match


async def fetch_appointments(user_id: str) -> list[AppointmentRecordSchema]:
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            result = await client.call_tool(
                "get_appointments",
                {"data": {"user_id": user_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"appointment_scheduler_agent unreachable: {exc}") from exc

    records = result.structured_content if isinstance(result.structured_content, list) else []
    return [AppointmentRecordSchema(**r) for r in records]
