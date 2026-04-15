from datetime import datetime, timezone

from typing_extensions import Annotated
from pydantic import BaseModel, Field, AfterValidator


def validate_not_future(analysis_datetime: datetime) -> datetime:
    normalized = analysis_datetime
    if analysis_datetime.tzinfo is None:
        normalized = analysis_datetime.replace(tzinfo=timezone.utc)
    else:
        normalized = analysis_datetime.astimezone(timezone.utc)
    if normalized > datetime.now(timezone.utc):
        raise ValueError("datetime must be now or in the past")
    return normalized


AnalysisDate = Annotated[
    datetime,
    AfterValidator(validate_not_future),
    Field(
        description="ISO 8601 UTC datetime of the lab result. Must be now or in the past.",
        format="date-time",
    ),
]


class PatientAnalysis(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    analysis_text: str = Field(
        description="Raw or structured text of the lab results, e.g. 'Glucose: 105 mg/dL, HbA1c: 5.7%'."
    )
    analysis_date: AnalysisDate
    created_at: datetime
