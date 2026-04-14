import uuid

from loguru import logger
from sqlalchemy import select, update

from db.engine import SessionLocal
from db.models import Complaint, COMPLAINT_STATUS_READ, COMPLAINT_STATUS_APPOINTMENT
from schemas.complaint import MarkAsReadRequest, MutateComplaintResponse


async def mark_as_read(request: MarkAsReadRequest) -> MutateComplaintResponse:
    try:
        complaint_id = uuid.UUID(request.complaint_id)
    except ValueError:
        return MutateComplaintResponse(success=False, error=f"Invalid complaint_id: {request.complaint_id}")

    async with SessionLocal() as session:
        result = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
        existing = result.scalar_one_or_none()
        if existing is None:
            return MutateComplaintResponse(success=False, error=f"Complaint {complaint_id} not found")

        if existing.status == COMPLAINT_STATUS_APPOINTMENT:
            return MutateComplaintResponse(success=True)

        await session.execute(
            update(Complaint)
            .where(Complaint.id == complaint_id)
            .values(status=COMPLAINT_STATUS_READ)
        )
        await session.commit()

    logger.info(f"Complaint marked as read: {complaint_id}")
    return MutateComplaintResponse(success=True)
