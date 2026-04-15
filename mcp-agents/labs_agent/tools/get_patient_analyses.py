from datetime import timezone

from loguru import logger
from sqlalchemy import or_, select

from db.engine import SessionLocal
from db.models import PatientAnalysis as PatientAnalysisRow
from schemas.http import GetPatientAnalysesRequest, GetPatientAnalysisRecord


async def get_patient_analyses(data: GetPatientAnalysesRequest) -> list[GetPatientAnalysisRecord]:
    start_date = data.start_date
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    else:
        start_date = start_date.astimezone(timezone.utc)
    logger.info(f"Fetching analyses: user={data.user_id}, from={start_date}")

    query = (
        select(PatientAnalysisRow)
        .where(PatientAnalysisRow.user_id == data.user_id)
        .where(
            or_(
                PatientAnalysisRow.analysis_date >= start_date,
                PatientAnalysisRow.analysis_date.is_(None),
            )
        )
        .order_by(PatientAnalysisRow.analysis_date.asc().nullslast())
    )

    async with SessionLocal() as session:
        result = await session.execute(query)
        rows = result.scalars().all()

    records = [
        GetPatientAnalysisRecord(
            analysis_id=str(row.id),
            user_id=row.user_id,
            analysis_text=row.analysis_text,
            analysis_date=row.analysis_date.isoformat() if row.analysis_date else None,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]

    logger.info(f"Found {len(records)} analysis record(s)")
    return records
