import uuid

from loguru import logger
from sqlalchemy import insert

from db.engine import SessionLocal
from db.models import PatientHistory
from schemas.http import RecordPatientHistoryResponse
from schemas.patient_history import PatientHistoryRecord


async def add_patient_history(data: PatientHistoryRecord) -> RecordPatientHistoryResponse:
    history_id = uuid.uuid4()

    logger.info(
        f"Recording patient history: user={data.user_id}, specialty={data.doctor_type.value}, date={data.history_date}"
    )

    async with SessionLocal() as session:
        await session.execute(
            insert(PatientHistory).values(
                id=history_id,
                user_id=data.user_id,
                doctor_type=data.doctor_type.value,
                history_date=data.history_date,
                subjective=data.subjective,
                objective=data.objective,
                assessment=data.assessment,
                plan=data.plan or "",
            )
        )
        await session.commit()

    logger.info(f"Patient history recorded: history_id={history_id}")
    return RecordPatientHistoryResponse(success=True, history_id=str(history_id))
