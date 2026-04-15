import uuid
from datetime import timezone

from loguru import logger
from sqlalchemy import select, update

from db.engine import SessionLocal
from db.models import PatientAnalysis as PatientAnalysisRow
from schemas.http import UpdateAnalysisRequest, UpdateAnalysisResponse


async def update_analysis(data: UpdateAnalysisRequest) -> UpdateAnalysisResponse:
    try:
        analysis_id = uuid.UUID(data.analysis_id)
    except ValueError:
        msg = f"Invalid analysis_id format: {data.analysis_id}"
        logger.error(msg)
        return UpdateAnalysisResponse(success=False, error=msg)

    async with SessionLocal() as session:
        result = await session.execute(
            select(PatientAnalysisRow).where(PatientAnalysisRow.id == analysis_id)
        )
        if result.scalar_one_or_none() is None:
            msg = f"Analysis {analysis_id} not found"
            logger.error(msg)
            return UpdateAnalysisResponse(success=False, error=msg)

        values: dict = {}
        if data.analysis_text is not None:
            values["analysis_text"] = data.analysis_text.strip() or None
        if data.analysis_date is not None:
            if data.analysis_date.tzinfo is None:
                values["analysis_date"] = data.analysis_date.replace(tzinfo=timezone.utc)
            else:
                values["analysis_date"] = data.analysis_date.astimezone(timezone.utc)

        if values:
            await session.execute(
                update(PatientAnalysisRow)
                .where(PatientAnalysisRow.id == analysis_id)
                .values(**values)
            )
            await session.commit()

    logger.info(f"Analysis updated: {analysis_id}")
    return UpdateAnalysisResponse(success=True)
