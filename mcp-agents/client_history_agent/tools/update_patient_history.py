import sys
import uuid

from loguru import logger
from sqlalchemy import select, update

from db.engine import SessionLocal
from db.models import PatientHistory
from schemas.http import UpdatePatientHistoryRequest, UpdatePatientHistoryResponse

logger.add(sys.stderr, level="INFO")


async def update_patient_history(data: UpdatePatientHistoryRequest) -> UpdatePatientHistoryResponse:
    try:
        history_id = uuid.UUID(data.history_id)
    except ValueError:
        msg = f"Invalid history_id format: {data.history_id}"
        logger.error(msg)
        return UpdatePatientHistoryResponse(success=False, error=msg)

    async with SessionLocal() as session:
        result = await session.execute(select(PatientHistory).where(PatientHistory.id == history_id))
        if result.scalar_one_or_none() is None:
            msg = f"Patient history record {history_id} not found"
            logger.error(msg)
            return UpdatePatientHistoryResponse(success=False, error=msg)

        await session.execute(
            update(PatientHistory)
            .where(PatientHistory.id == history_id)
            .values(
                history_date=data.history_date,
                subjective=data.subjective,
                objective=data.objective,
                assessment=data.assessment,
                plan=data.plan,
            )
        )
        await session.commit()

    logger.info(f"Patient history updated: {history_id}")
    return UpdatePatientHistoryResponse(success=True)
