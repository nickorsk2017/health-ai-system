from datetime import date

from typing_extensions import Annotated
from pydantic import BaseModel, Field, AfterValidator


def validate_not_future(analysis_date: date) -> date:
    if analysis_date > date.today():
        raise ValueError("date must be today or in the past")
    return analysis_date


AnalysisDate = Annotated[
    date,
    AfterValidator(validate_not_future),
    Field(
        description="ISO 8601 date of the lab result (YYYY-MM-DD). Must be today or in the past.",
        format="date",
    ),
]


class PatientAnalysis(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    analysis: str = Field(
        description="Raw or structured text of the lab results, e.g. 'Glucose: 105 mg/dL, HbA1c: 5.7%'."
    )
    date: AnalysisDate
    created_at: str = Field(
        default="",
        description="ISO 8601 timestamp when the record was created.",
    )
