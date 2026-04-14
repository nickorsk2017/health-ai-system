from datetime import date
from enum import Enum
from typing_extensions import Annotated
from pydantic import BaseModel, Field, AfterValidator


class DoctorType(str, Enum):
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


def validate_not_past(history_date: date) -> date:
    if history_date > date.today():
        raise ValueError("date must be today or past")
    return history_date


HistoryDate = Annotated[
    date,
    AfterValidator(validate_not_past),
    Field(
        description="YYYY-MM-DD, Date of the medical visit in ISO 8601 format (YYYY-MM-DD). Must be today or in the past.",
        format="date",
    )
]


class PatientHistoryRecord(BaseModel):
    history_id: str | None = Field(description="Unique identifier for the patient history record.")
    user_id: str = Field(description="Identifier of the patient.")
    doctor_type: DoctorType = Field(description="Medical specialty of the consulted physician.")
    history_date: HistoryDate
    subjective: str = Field(description="Patient's complaints, history, and symptoms as reported.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="(Optional) Treatment plan or next steps.")
    created_at: str = Field(
        default="",
        description="ISO 8601 timestamp when the record was created."
    )
