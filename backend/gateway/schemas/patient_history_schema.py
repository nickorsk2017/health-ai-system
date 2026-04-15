from datetime import datetime

from pydantic import BaseModel, Field

from _common.models.visit import DoctorType, PatientHistoryRecord

# Backward-compatible aliases
DoctorTypeSchema = DoctorType
PatientHistoryRecordSchema = PatientHistoryRecord


class CreatePatientHistorySchema(BaseModel):
    user_id: str = Field(description="Patient identifier.")
    doctor_type: DoctorType
    history_date: datetime = Field(description="ISO 8601 UTC datetime of the consultation.")
    subjective: str = Field(description="Patient complaints, history, and symptoms.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="Treatment plan or next steps.")


class RecordPatientHistoryResponseSchema(BaseModel):
    success: bool
    history_id: str


class HistoryFromPromptRequestSchema(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text clinical notes to be parsed into SOAP records.")


class HistoryFromPromptResponseSchema(BaseModel):
    success: bool
    count: int = Field(description="Number of patient history records created.")


class UpdatePatientHistorySchema(BaseModel):
    history_date: datetime = Field(description="ISO 8601 UTC datetime of the consultation.")
    subjective: str
    objective: str
    assessment: str
    plan: str = ""


class MutatePatientHistoryResponseSchema(BaseModel):
    success: bool


__all__ = [
    "DoctorType",
    "DoctorTypeSchema",
    "PatientHistoryRecord",
    "PatientHistoryRecordSchema",
    "CreatePatientHistorySchema",
    "RecordPatientHistoryResponseSchema",
    "HistoryFromPromptRequestSchema",
    "HistoryFromPromptResponseSchema",
    "UpdatePatientHistorySchema",
    "MutatePatientHistoryResponseSchema",
]
