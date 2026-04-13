from fastapi import APIRouter, HTTPException

from schemas.visit_schema import CreateVisitSchema, RecordVisitResponseSchema
from services.exceptions import AgentConnectionError, NoDataFoundError
from services.visit_doctor_service import record_visit

router = APIRouter(prefix="/api/v1/visits", tags=["visits"])


@router.post("", response_model=RecordVisitResponseSchema, status_code=201)
async def create_visit(body: CreateVisitSchema) -> RecordVisitResponseSchema:
    try:
        return await record_visit(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
