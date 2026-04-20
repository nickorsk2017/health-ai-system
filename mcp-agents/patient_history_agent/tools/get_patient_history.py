from datetime import timezone

from loguru import logger
from sqlalchemy import select

from db.engine import SessionLocal
from db.models import PatientHistory
from schemas.patient_history import DoctorType, PatientHistoryRecord
from schemas.http import GetPatientHistoryRequest


async def get_patient_history(
    data: GetPatientHistoryRequest,
) -> list[PatientHistoryRecord]:
    last_history_date = data.last_history_date
    if last_history_date.tzinfo is None:
        last_history_date = last_history_date.replace(tzinfo=timezone.utc)
    else:
        last_history_date = last_history_date.astimezone(timezone.utc)
    logger.info(
        f"Fetching patient history: user={data.user_id}, from={last_history_date}, specialty={data.doctor_type if data.doctor_type else 'all'}"
    )

    query = (
        select(PatientHistory)
        .where(PatientHistory.user_id == data.user_id)
        .where(PatientHistory.history_date >= last_history_date)
        .order_by(PatientHistory.history_date.desc())
    )

    if data.doctor_type is not None and data.doctor_type != "":
        query = query.where(PatientHistory.doctor_type == data.doctor_type)

    async with SessionLocal() as session:
        result = await session.execute(query)
        rows = result.scalars().all()

    records = [
        PatientHistoryRecord(
            history_id=str(row.id),
            user_id=row.user_id,
            doctor_type=DoctorType(row.doctor_type),
            history_date=row.history_date.isoformat(),
            subjective=row.subjective,
            objective=row.objective,
            assessment=row.assessment,
            plan=row.plan,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]

    logger.info(f"Found {len(records)} patient history record(s)")
    return records
