from enum import Enum

from pydantic import BaseModel, Field


class DoctorTypeSchema(str, Enum):
    oncology = "oncology"
    gastroenterology = "gastroenterology"
    cardiology = "cardiology"
    hematology = "hematology"
    nephrology = "nephrology"
    nutrition = "nutrition"
    endocrinology = "endocrinology"
    mental_health = "mental_health"
    pulmonology = "pulmonology"
    general_practitioner = "general_practitioner"


class CreatePatientHistorySchema(BaseModel):
    user_id: str = Field(description="Patient identifier.")
    doctor_type: DoctorTypeSchema
    history_date: str = Field(description="ISO 8601 date of the consultation (YYYY-MM-DD).")
    subjective: str = Field(description="Patient complaints, history, and symptoms.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="Treatment plan or next steps.")


class RecordPatientHistoryResponseSchema(BaseModel):
    success: bool
    history_id: str


class PatientHistoryRecordSchema(BaseModel):
    history_id: str
    user_id: str
    doctor_type: str
    history_date: str
    subjective: str
    objective: str
    assessment: str
    plan: str = ""
    created_at: str = ""


class HistoryFromPromptRequestSchema(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text clinical notes to be parsed into SOAP records.")


class HistoryFromPromptResponseSchema(BaseModel):
    success: bool
    count: int = Field(description="Number of patient history records created.")


class UpdatePatientHistorySchema(BaseModel):
    history_date: str = Field(description="ISO 8601 date of the consultation (YYYY-MM-DD).")
    subjective: str
    objective: str
    assessment: str
    plan: str = ""


class MutatePatientHistoryResponseSchema(BaseModel):
    success: bool
