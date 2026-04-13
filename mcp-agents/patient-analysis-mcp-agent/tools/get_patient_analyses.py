from loguru import logger
from sqlalchemy import select

from db.engine import SessionLocal
from db.models import PatientAnalysis as PatientAnalysisRow
from schemas.analysis import PatientAnalysis
from schemas.http import GetPatientAnalysesRequest


async def get_patient_analyses(data: GetPatientAnalysesRequest) -> list[PatientAnalysis]:
    logger.info(f"Fetching analyses: user={data.user_id}, from={data.start_date}")

    query = (
        select(PatientAnalysisRow)
        .where(PatientAnalysisRow.user_id == data.user_id)
        .where(PatientAnalysisRow.analysis_date >= data.start_date)
        .order_by(PatientAnalysisRow.analysis_date.asc())
    )

    async with SessionLocal() as session:
        result = await session.execute(query)
        rows = result.scalars().all()

    analyses = [
        PatientAnalysis(
            user_id=row.user_id,
            analysis=row.analysis_text,
            date=row.analysis_date,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]

    logger.info(f"Found {len(analyses)} analysis record(s)")
    return analyses
