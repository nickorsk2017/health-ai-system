import uuid

from loguru import logger
from sqlalchemy import delete, select

from db.engine import SessionLocal
from db.models import PatientAnalysis as PatientAnalysisRow
from schemas.http import DeleteAnalysisRequest, DeleteAnalysisResponse


async def delete_analysis(data: DeleteAnalysisRequest) -> DeleteAnalysisResponse:
    try:
        analysis_id = uuid.UUID(data.analysis_id)
    except ValueError:
        msg = f"Invalid analysis_id format: {data.analysis_id}"
        logger.error(msg)
        return DeleteAnalysisResponse(success=False, error=msg)

    async with SessionLocal() as session:
        result = await session.execute(
            select(PatientAnalysisRow).where(PatientAnalysisRow.id == analysis_id)
        )
        if result.scalar_one_or_none() is None:
            msg = f"Analysis {analysis_id} not found"
            logger.error(msg)
            return DeleteAnalysisResponse(success=False, error=msg)

        await session.execute(
            delete(PatientAnalysisRow).where(PatientAnalysisRow.id == analysis_id)
        )
        await session.commit()

    logger.info(f"Analysis deleted: {analysis_id}")
    return DeleteAnalysisResponse(success=True)
