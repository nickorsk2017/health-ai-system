import uuid
from datetime import timezone

from loguru import logger
from sqlalchemy import insert, select, text

from db.engine import SessionLocal
from db.models import Appointment
from schemas.appointment import AppointmentRecord, CreateAppointmentRequest, CreateAppointmentResponse


async def create_appointment(request: CreateAppointmentRequest) -> CreateAppointmentResponse:
    try:
        complaint_id = uuid.UUID(request.complaint_id)
    except ValueError:
        return CreateAppointmentResponse(
            success=False, error=f"Invalid complaint_id: {request.complaint_id}"
        )
    try:
        user_id = uuid.UUID(request.user_id)
    except ValueError:
        return CreateAppointmentResponse(
            success=False, error=f"Invalid user_id: {request.user_id}"
        )

    appointment_date = request.appointment_date
    if appointment_date.tzinfo is None:
        appointment_date = appointment_date.replace(tzinfo=timezone.utc)
    else:
        appointment_date = appointment_date.astimezone(timezone.utc)

    appointment_id = uuid.uuid4()

    async with SessionLocal() as session:
        await session.execute(
            insert(Appointment).values(
                id=appointment_id,
                complaint_id=complaint_id,
                user_id=user_id,
                appointment_date=appointment_date,
                doctor_type=request.doctor_type,
                problem_notes=request.problem_notes,
            )
        )
        await session.execute(
            text("UPDATE complaints SET status = 'appointment' WHERE id = :complaint_id"),
            {"complaint_id": complaint_id},
        )
        await session.commit()
        row = await session.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        created = row.scalar_one()
        record = AppointmentRecord(
            appointment_id=str(created.id),
            complaint_id=str(created.complaint_id),
            user_id=str(created.user_id),
            appointment_date=created.appointment_date,
            doctor_type=created.doctor_type,
            problem_notes=created.problem_notes or "",
            created_at=created.created_at,
        )

    logger.info(f"Appointment created: {appointment_id} for complaint {complaint_id}")
    return CreateAppointmentResponse(success=True, appointment_id=str(appointment_id), record=record)
