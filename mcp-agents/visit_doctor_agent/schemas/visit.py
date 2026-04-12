from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


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


class DoctorVisit(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    doctor_type: DoctorType = Field(description="Medical specialty of the consulted physician.")
    date_visit: date = Field(
        description="ISO 8601 date of the consultation (YYYY-MM-DD)",
        format="date"
    )
    subjective: str = Field(description="Patient's complaints, history, and symptoms as reported.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default=None, description="Treatment plan or next steps.")
    created_at: str | None = Field(default=None, description="ISO 8601 timestamp when the record was created.")

    @field_validator("date_visit")
    @classmethod
    def date_visit_not_in_past(cls, date_visit: date) -> date:
        if date_visit < date.today():
            raise ValueError(f"date_visit must be today or in the future, got {date_visit}")
        return date_visit
