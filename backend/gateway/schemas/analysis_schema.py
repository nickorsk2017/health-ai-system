from datetime import date

from pydantic import BaseModel, Field


class AnalysisRequestSchema(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    analysis_text: str = Field(
        description="Raw or structured text of the lab results, e.g. 'Glucose: 105 mg/dL, HbA1c: 5.7%'."
    )
    analysis_date: date = Field(description="ISO 8601 date of the lab result (YYYY-MM-DD).")


class AnalysisResponseSchema(BaseModel):
    success: bool


class AnalysisRecordSchema(BaseModel):
    analysis_id: str
    user_id: str
    analysis_text: str | None = None
    analysis_date: str | None = None
    created_at: str


class UpdateAnalysisSchema(BaseModel):
    analysis_text: str | None = None
    analysis_date: str | None = None


class MutateAnalysisResponseSchema(BaseModel):
    success: bool


class AnalysisByPromptRequestSchema(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text lab notes to be parsed into analysis records.")


class AnalysisByPromptResponseSchema(BaseModel):
    success: bool
    list_missing_analysis: list[str] = Field(default_factory=list)
