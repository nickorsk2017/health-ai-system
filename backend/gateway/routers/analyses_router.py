from fastapi import APIRouter, HTTPException, Query

from schemas.analysis_schema import AnalysisRecordSchema, AnalysisRequestSchema, AnalysisResponseSchema
from services.analysis_service import fetch_analyses, record_analysis
from services.exceptions import AgentConnectionError, NoDataFoundError

router = APIRouter(prefix="/api/v1/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResponseSchema, status_code=201)
async def add_analysis(body: AnalysisRequestSchema) -> AnalysisResponseSchema:
    try:
        return await record_analysis(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("/{user_id}", response_model=list[AnalysisRecordSchema])
async def get_analyses(
    user_id: str,
    start_date: str = Query(
        default="2000-01-01",
        description="ISO 8601 start date (YYYY-MM-DD). Returns all analyses from this date onward.",
    ),
) -> list[AnalysisRecordSchema]:
    try:
        return await fetch_analyses(user_id, start_date)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError:
        return []
