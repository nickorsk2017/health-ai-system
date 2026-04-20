from datetime import datetime

from pydantic import BaseModel, Field
from schemas.patient_history import PatientHistoryRecord


class RecordPatientHistoryResponse(BaseModel):
    success: bool
    history_id: str


class GetPatientHistoryResponse(BaseModel):
    records: list[PatientHistoryRecord]


class GetPatientHistoryRequest(BaseModel):
    last_history_date: datetime = Field(
        description="ISO 8601 UTC datetime lower bound for medical visits.",
        format="date-time",
    )
    user_id: str
    doctor_type: str = Field(
        default="",
        description="(Optional) Medical specialty to filter by. If not provided, returns all specialties.",
    )


class CreateHistoryFromPromptRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text clinical notes describing one or more medical visits.")


class CreateHistoryFromPromptResponse(BaseModel):
    success: bool
    count: int = Field(description="Number of patient history records created.")


class UpdatePatientHistoryRequest(BaseModel):
    history_id: str = Field(description="UUID of the patient history record to update.")
    history_date: datetime = Field(description="ISO 8601 UTC datetime of the consultation.")
    subjective: str = Field(description="Patient complaints, history, and symptoms.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="Treatment plan or next steps.")


class UpdatePatientHistoryResponse(BaseModel):
    success: bool
    error: str = ""


class DeletePatientHistoryRequest(BaseModel):
    history_id: str = Field(description="UUID of the patient history record to delete.")


class DeletePatientHistoryResponse(BaseModel):
    success: bool
    error: str = ""
