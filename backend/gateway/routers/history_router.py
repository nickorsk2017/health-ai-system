from fastapi import APIRouter, HTTPException, Query

from schemas.visit_schema import VisitRecordSchema
from services.exceptions import AgentConnectionError, NoDataFoundError
from services.visit_doctor_service import fetch_visit_history

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("/{user_id}", response_model=list[VisitRecordSchema])
async def get_history(
    user_id: str,
    last_date_visit: str = Query(description="ISO 8601 date (YYYY-MM-DD). Returns visits from this date onward."),
) -> list[VisitRecordSchema]:
    try:
        return await fetch_visit_history(user_id, last_date_visit)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
