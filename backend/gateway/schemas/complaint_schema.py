from datetime import datetime

from pydantic import BaseModel

from _common.models.complaint import ComplaintRecord, ComplaintStatus

# Backward-compatible aliases
ComplaintRecordSchema = ComplaintRecord


class UpsertComplaintSchema(BaseModel):
    user_id: str
    problem_health: str
    date_public: datetime


class ComplaintsByPromptRequestSchema(BaseModel):
    user_id: str
    prompt: str


__all__ = [
    "ComplaintStatus",
    "ComplaintRecord",
    "ComplaintRecordSchema",
    "UpsertComplaintSchema",
    "ComplaintsByPromptRequestSchema",
]
