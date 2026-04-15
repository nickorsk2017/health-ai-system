from typing import Literal

from pydantic import BaseModel, ConfigDict

ComplaintStatus = Literal["unread", "read", "appointment"]


class ComplaintRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    complaint_id: str
    user_id: str
    problem_health: str
    date_public: str
    status: ComplaintStatus
    created_at: str
