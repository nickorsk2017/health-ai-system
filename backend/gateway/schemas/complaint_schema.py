from pydantic import BaseModel

from _common.models.complaint import ComplaintRecord, ComplaintStatus

# Backward-compatible aliases
ComplaintRecordSchema = ComplaintRecord


class UpsertComplaintSchema(BaseModel):
    user_id: str
    problem_health: str
    date_public: str


__all__ = [
    "ComplaintStatus",
    "ComplaintRecord",
    "ComplaintRecordSchema",
    "UpsertComplaintSchema",
]
