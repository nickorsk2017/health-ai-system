import datetime
from pydantic import BaseModel, Field
from schemas.consilium import SpecialistFinding 

class ConsiliumResponse(BaseModel):
    findings: list[SpecialistFinding] = Field(
        description="Findings from all specialties that identified relevant issues."
    )


class GetDoctorVisitsHistoryRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: datetime.date = Field(
        description="ISO 8601 start date for history retrieval (YYYY-MM-DD)."
    )   