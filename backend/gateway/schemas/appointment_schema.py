from pydantic import BaseModel

from _common.models.appointment import AppointmentRecord

# Backward-compatible alias
AppointmentRecordSchema = AppointmentRecord


class CreateAppointmentSchema(BaseModel):
    complaint_id: str
    user_id: str
    appointment_date: str
    doctor_type: str
    problem_notes: str = ""


__all__ = [
    "AppointmentRecord",
    "AppointmentRecordSchema",
    "CreateAppointmentSchema",
]
