import uuid

from loguru import logger
from sqlalchemy import delete, select

from db.engine import SessionLocal
from db.models import Complaint
from schemas.complaint import DeleteComplaintRequest, MutateComplaintResponse


async def delete_complaint(request: DeleteComplaintRequest) -> MutateComplaintResponse:
    try:
        complaint_id = uuid.UUID(request.complaint_id)
    except ValueError:
        return MutateComplaintResponse(success=False, error=f"Invalid complaint_id: {request.complaint_id}")

    async with SessionLocal() as session:
        result = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
        if result.scalar_one_or_none() is None:
            return MutateComplaintResponse(success=False, error=f"Complaint {complaint_id} not found")

        await session.execute(delete(Complaint).where(Complaint.id == complaint_id))
        await session.commit()

    logger.info(f"Complaint deleted: {complaint_id}")
    return MutateComplaintResponse(success=True)
