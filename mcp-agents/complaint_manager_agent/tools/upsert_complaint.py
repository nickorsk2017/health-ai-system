import uuid
from datetime import date

from loguru import logger
from sqlalchemy import insert, select, update

from db.engine import SessionLocal
from db.models import Complaint, COMPLAINT_STATUS_UNREAD
from schemas.complaint import UpsertComplaintRequest, UpsertComplaintResponse


async def upsert_complaint(request: UpsertComplaintRequest) -> UpsertComplaintResponse:
    date_public = date.fromisoformat(request.date_public)

    if request.complaint_id:
        complaint_id = uuid.UUID(request.complaint_id)
        async with SessionLocal() as session:
            result = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
            existing = result.scalar_one_or_none()
            if existing is None:
                return UpsertComplaintResponse(success=False, complaint_id="")
            await session.execute(
                update(Complaint)
                .where(Complaint.id == complaint_id)
                .values(problem_health=request.problem_health, date_public=date_public)
            )
            await session.commit()
        logger.info(f"Complaint updated: {complaint_id}")
        return UpsertComplaintResponse(success=True, complaint_id=str(complaint_id))

    complaint_id = uuid.uuid4()
    async with SessionLocal() as session:
        await session.execute(
            insert(Complaint).values(
                id=complaint_id,
                user_id=request.user_id,
                problem_health=request.problem_health,
                date_public=date_public,
                status=COMPLAINT_STATUS_UNREAD,
            )
        )
        await session.commit()

    logger.info(f"Complaint created: {complaint_id} for user {request.user_id}")
    return UpsertComplaintResponse(success=True, complaint_id=str(complaint_id))
