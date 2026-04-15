import uuid
from datetime import timezone

from loguru import logger
from sqlalchemy import insert

from db.engine import SessionLocal
from db.models import PatientAnalysis as PatientAnalysisRow
from schemas.analysis import PatientAnalysis
from schemas.http import AddPatientAnalysisResponse


async def add_patient_analysis(data: PatientAnalysis) -> AddPatientAnalysisResponse:
    analysis_id = uuid.uuid4()
    analysis_date = data.analysis_date
    if analysis_date.tzinfo is None:
        analysis_date = analysis_date.replace(tzinfo=timezone.utc)
    else:
        analysis_date = analysis_date.astimezone(timezone.utc)

    logger.info(f"Recording analysis: user={data.user_id}, date={data.analysis_date}")

    async with SessionLocal() as session:
        await session.execute(
            insert(PatientAnalysisRow).values(
                id=analysis_id,
                user_id=data.user_id,
                analysis_text=data.analysis_text,
                analysis_date=analysis_date,
            )
        )
        await session.commit()

    logger.info(f"Analysis recorded: analysis_id={analysis_id}")
    return AddPatientAnalysisResponse(success=True)
