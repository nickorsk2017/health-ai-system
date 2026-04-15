from pydantic import BaseModel, ConfigDict


class AppointmentRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    appointment_id: str
    complaint_id: str
    user_id: str
    appointment_date: str
    doctor_type: str
    problem_notes: str
    created_at: str
