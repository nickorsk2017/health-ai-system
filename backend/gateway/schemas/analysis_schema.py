from datetime import date

from pydantic import BaseModel, Field


class AnalysisRequestSchema(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    analysis: str = Field(
        description="Raw or structured text of the lab results, e.g. 'Glucose: 105 mg/dL, HbA1c: 5.7%'."
    )
    analysis_date: date = Field(description="ISO 8601 date of the lab result (YYYY-MM-DD).")


class AnalysisResponseSchema(BaseModel):
    success: bool


class AnalysisRecordSchema(BaseModel):
    user_id: str
    analysis: str
    date: date
    created_at: str
