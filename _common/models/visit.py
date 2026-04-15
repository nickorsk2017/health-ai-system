from datetime import datetime, timezone
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


def _validate_not_future(history_datetime: datetime) -> datetime:
    normalized = history_datetime
    if history_datetime.tzinfo is None:
        normalized = history_datetime.replace(tzinfo=timezone.utc)
    else:
        normalized = history_datetime.astimezone(timezone.utc)
    if normalized > datetime.now(timezone.utc):
        raise ValueError("datetime must be now or in the past")
    return normalized


HistoryDate = Annotated[
    datetime,
    AfterValidator(_validate_not_future),
    Field(
        description="ISO 8601 UTC datetime of the medical visit. Must be now or in the past.",
        format="date-time",
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
    created_at: datetime | None = Field(
        default=None,
        description="ISO 8601 UTC timestamp",
    )
