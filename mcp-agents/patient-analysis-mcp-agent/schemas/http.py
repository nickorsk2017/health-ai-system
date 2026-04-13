from datetime import date

from pydantic import BaseModel, Field


class AddPatientAnalysisResponse(BaseModel):
    success: bool


class GetPatientAnalysesRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: date = Field(
        description="ISO 8601 start date for the search (YYYY-MM-DD).",
        format="date",
    )
