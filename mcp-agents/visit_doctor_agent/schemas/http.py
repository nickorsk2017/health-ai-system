
from datetime import date

from pydantic import BaseModel, Field
from schemas.visit import DoctorVisit



class RecordDoctorVisitResponse(BaseModel):
    success: bool
    visit_id: str


class GetDoctorVisitsHistoryResponse(BaseModel):
    records: list[DoctorVisit]

class GetDoctorVisitsHistoryRequest(BaseModel):
    last_date_visit: date = Field(description="YYYY-MM-DD, Date of the medical visit in ISO 8601 format (YYYY-MM-DD). Must be today or in the past.", format="date",)
    user_id: str
    doctor_type: str = Field(default="", description="(Optional) Medical specialty to filter visits by. If not provided, returns visits of all specialties.")