from datetime import date

from pydantic import BaseModel, Field

from _common.models.analysis import AnalysisRecord

# Backward-compatible alias used by existing tool files
GetPatientAnalysisRecord = AnalysisRecord


class AddPatientAnalysisResponse(BaseModel):
    success: bool


class GetPatientAnalysesRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: date = Field(
        description="ISO 8601 start date for the search (YYYY-MM-DD).",
        format="date",
    )


class UpdateAnalysisRequest(BaseModel):
    analysis_id: str = Field(description="UUID of the analysis record to update.")
    analysis_text: str | None = Field(default=None, description="Updated lab result text.")
    analysis_date: str | None = Field(default=None, description="Updated ISO 8601 date YYYY-MM-DD.")


class UpdateAnalysisResponse(BaseModel):
    success: bool
    error: str = ""


class DeleteAnalysisRequest(BaseModel):
    analysis_id: str = Field(description="UUID of the analysis record to delete.")


class DeleteAnalysisResponse(BaseModel):
    success: bool
    error: str = ""


class CreateAnalysesFromPromptRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text lab notes to be parsed into analysis records.")


class CreateAnalysesFromPromptResponse(BaseModel):
    success: bool
    list_missing_analysis: list[str] = Field(
        default_factory=list,
        description="Raw text of entries that had missing analysis_text or analysis_date.",
    )


__all__ = [
    "AnalysisRecord",
    "GetPatientAnalysisRecord",
    "AddPatientAnalysisResponse",
    "GetPatientAnalysesRequest",
    "UpdateAnalysisRequest",
    "UpdateAnalysisResponse",
    "DeleteAnalysisRequest",
    "DeleteAnalysisResponse",
    "CreateAnalysesFromPromptRequest",
    "CreateAnalysesFromPromptResponse",
]
