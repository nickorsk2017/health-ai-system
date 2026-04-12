from pydantic import BaseModel, Field


class SpecialistAnalysis(BaseModel):
    """Structured LLM output for a single specialty review."""

    is_relevant: bool = Field(
        description=(
            "True if the patient history contains findings relevant to this specialty "
            "and a meaningful analysis can be provided. False if the history is insufficient "
            "or entirely unrelated to this specialty."
        )
    )
    risks: str = Field(
        default="",
        description="Key risk factors identified from the patient history (2-3 sentences).",
    )
    treatment: str = Field(
        default="",
        description="Recommended treatment approach or management strategy (2-3 sentences).",
    )
    prognosis: str = Field(
        default="",
        description="Expected clinical outcome and prognosis based on available data (2-3 sentences).",
    )
    probable_diagnosis: str = Field(
        default="",
        description="Most probable diagnosis or differential diagnoses (2-3 sentences).",
    )


class SpecialistFinding(BaseModel):
    specialty: str = Field(description="Medical specialty that produced this finding.")
    risks: str
    treatment: str
    prognosis: str
    probable_diagnosis: str
