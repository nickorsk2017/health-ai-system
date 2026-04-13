
from datetime import date
from pydantic import BaseModel, Field  

class GetSynthesisRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: date = Field(
        description="ISO 8601 start date for history retrieval (YYYY-MM-DD)."
    )
    analyses: list[str] = Field(
        default_factory=list,
        description="Optional list of laboratory test result texts to include in the synthesis.",
    )   