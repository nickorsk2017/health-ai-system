from pydantic import BaseModel

from schemas.visit import DoctorVisit


class RecordDoctorVisitResponse(BaseModel):
    success: bool
    visit_id: str


class GetDoctorVisitsHistoryResponse(BaseModel):
    records: list[DoctorVisit]
