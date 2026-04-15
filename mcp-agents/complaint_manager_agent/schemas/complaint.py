from datetime import datetime

from _common.models.complaint import ComplaintRecord, ComplaintStatus

from pydantic import BaseModel, Field


class UpsertComplaintRequest(BaseModel):
    user_id: str = Field(description="UUID of the patient submitting the complaint.")
    problem_health: str = Field(description="Description of the symptom or health problem.")
    date_public: datetime = Field(description="ISO 8601 UTC datetime when the patient reported this complaint.")
    complaint_id: str | None = Field(
        default=None,
        description="UUID of an existing complaint to update. Omit to create a new one.",
    )


class UpsertComplaintResponse(BaseModel):
    success: bool
    complaint_id: str
    complaint: "ComplaintRecord | None" = None


class GetComplaintsRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        description="Patient UUID to filter complaints by.",
    )


class MarkAsReadRequest(BaseModel):
    complaint_id: str = Field(description="UUID of the complaint to mark as read.")


class MutateComplaintResponse(BaseModel):
    success: bool
    error: str = ""


class DeleteComplaintRequest(BaseModel):
    complaint_id: str = Field(description="UUID of the complaint to delete.")


UpsertComplaintResponse.model_rebuild()

__all__ = [
    "ComplaintRecord",
    "ComplaintStatus",
    "UpsertComplaintRequest",
    "UpsertComplaintResponse",
    "GetComplaintsRequest",
    "MarkAsReadRequest",
    "MutateComplaintResponse",
    "DeleteComplaintRequest",
]
