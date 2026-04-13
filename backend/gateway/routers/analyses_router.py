from fastapi import APIRouter, HTTPException, Query

from schemas.analysis_schema import (
    AnalysisByPromptRequestSchema,
    AnalysisByPromptResponseSchema,
    AnalysisRecordSchema,
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    MutateAnalysisResponseSchema,
    UpdateAnalysisSchema,
)
from services.analysis_service import (
    create_analyses_from_prompt,
    delete_analysis,
    fetch_analyses,
    record_analysis,
    update_analysis,
)
from services.exceptions import AgentConnectionError, NoDataFoundError

router = APIRouter(prefix="/api/v1/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResponseSchema, status_code=201)
async def add_analysis(body: AnalysisRequestSchema) -> AnalysisResponseSchema:
    try:
        return await record_analysis(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.post("/by-prompt", response_model=AnalysisByPromptResponseSchema, status_code=201)
async def import_analyses_from_prompt(
    body: AnalysisByPromptRequestSchema,
) -> AnalysisByPromptResponseSchema:
    try:
        return await create_analyses_from_prompt(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.patch("/{analysis_id}", response_model=MutateAnalysisResponseSchema)
async def patch_analysis(
    analysis_id: str, body: UpdateAnalysisSchema
) -> MutateAnalysisResponseSchema:
    try:
        return await update_analysis(analysis_id, body)
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.delete("/{analysis_id}", response_model=MutateAnalysisResponseSchema)
async def remove_analysis(analysis_id: str) -> MutateAnalysisResponseSchema:
    try:
        return await delete_analysis(analysis_id)
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
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
