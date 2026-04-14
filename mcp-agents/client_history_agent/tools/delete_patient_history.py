import sys
import uuid

from loguru import logger
from sqlalchemy import delete, select

from db.engine import SessionLocal
from db.models import PatientHistory
from schemas.http import DeletePatientHistoryRequest, DeletePatientHistoryResponse

logger.add(sys.stderr, level="INFO")


async def delete_patient_history(data: DeletePatientHistoryRequest) -> DeletePatientHistoryResponse:
    try:
        history_id = uuid.UUID(data.history_id)
    except ValueError:
        msg = f"Invalid history_id format: {data.history_id}"
        logger.error(msg)
        return DeletePatientHistoryResponse(success=False, error=msg)

    async with SessionLocal() as session:
        result = await session.execute(select(PatientHistory).where(PatientHistory.id == history_id))
        if result.scalar_one_or_none() is None:
            msg = f"Patient history record {history_id} not found"
            logger.error(msg)
            return DeletePatientHistoryResponse(success=False, error=msg)

        await session.execute(delete(PatientHistory).where(PatientHistory.id == history_id))
        await session.commit()

    logger.info(f"Patient history deleted: {history_id}")
    return DeletePatientHistoryResponse(success=True)
