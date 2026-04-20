from datetime import timezone

from fastmcp import Client

from config import settings
from schemas.appointment_schema import AppointmentRecordSchema, CreateAppointmentSchema
from services.agent_result import AgentResult, to_response


async def create_appointment(data: CreateAppointmentSchema) -> AgentResult:
    appointment_date = data.appointment_date
    if appointment_date.tzinfo is None:
        appointment_date = appointment_date.replace(tzinfo=timezone.utc)
    else:
        appointment_date = appointment_date.astimezone(timezone.utc)
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            response = await client.call_tool(
                "create_appointment",
                {
                    "data": {
                        "complaint_id": data.complaint_id,
                        "user_id": data.user_id,
                        "appointment_date": appointment_date.isoformat(),
                        "doctor_type": data.doctor_type,
                        "problem_notes": data.problem_notes,
                    }
                },
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return to_response(error=raw_results.get("error", "appointment_scheduler_agent returned failure"))
        record = raw_results.get("record")
        appointment = AppointmentRecordSchema(**record) if record else None
        return to_response(data=appointment)
    except Exception as exc:
        return to_response(error=str(exc))


async def fetch_appointments(user_id: str) -> AgentResult:
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            response = await client.call_tool(
                "get_appointments",
                {"data": {"user_id": user_id}},
            )
        response_content = response.structured_content
        appointments_collection = (
            response_content.get("result") if isinstance(response_content, dict) else response_content
        ) or []
        return to_response(data=[AppointmentRecordSchema(**a) for a in appointments_collection])
    except Exception as exc:
        return to_response(error=str(exc))
