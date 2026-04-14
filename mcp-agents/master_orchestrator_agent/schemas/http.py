import datetime

from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: datetime.date = Field(
        description="ISO 8601 start date for data retrieval (YYYY-MM-DD)."
    )


class EvaluationResponse(BaseModel):
    findings: list[dict] = Field(
        description="SpecialistFinding objects produced by the MDT consilium."
    )
    history_available: bool = Field(
        description="True when SOAP history was successfully retrieved."
    )
    labs_available: bool = Field(
        description="True when laboratory data was successfully retrieved."
    )


class GPDiagnosisRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: datetime.date = Field(
        description="ISO 8601 start date for data retrieval (YYYY-MM-DD)."
    )


class GPDiagnosisResponse(BaseModel):
    consultation: dict = Field(
        description="GP consultation with diagnosis, treatment, prognosis, and summary."
    )
    history_available: bool = Field(
        description="True when SOAP history was successfully retrieved."
    )
    labs_available: bool = Field(
        description="True when laboratory data was successfully retrieved."
    )
    devices_available: bool = Field(
        description="True when device data was successfully retrieved."
    )
    complaints_available: bool = Field(
        description="True when complaint records were successfully retrieved."
    )
