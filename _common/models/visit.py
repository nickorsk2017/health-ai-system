from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic import AfterValidator
from typing_extensions import Annotated


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


def _validate_not_future(history_date: date) -> date:
    if history_date > date.today():
        raise ValueError("date must be today or in the past")
    return history_date


HistoryDate = Annotated[
    date,
    AfterValidator(_validate_not_future),
    Field(
        description="YYYY-MM-DD, Date of the medical visit in ISO 8601 format. Must be today or in the past.",
        format="date",
    ),
]


class PatientHistoryRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    history_id: str | None = Field(default=None, description="Unique identifier for the history record.")
    user_id: str = Field(description="Identifier of the patient.")
    doctor_type: DoctorType = Field(description="Medical specialty of the consulted physician.")
    history_date: HistoryDate
    subjective: str = Field(description="Patient's complaints, history, and symptoms as reported.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="Treatment plan or next steps.")
    created_at: str = Field(default="", description="ISO 8601 timestamp when the record was created.")
