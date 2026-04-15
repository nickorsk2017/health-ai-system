from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalysisRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    analysis_id: str
    user_id: str
    analysis_text: str | None = None
    analysis_date: datetime | None = None
    created_at: datetime
