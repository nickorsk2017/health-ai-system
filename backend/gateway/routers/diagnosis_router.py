from fastapi import APIRouter, HTTPException, Query

from schemas.diagnosis_schema import GPConsultationSchema
from services.exceptions import AgentConnectionError, NoDataFoundError
from services.gp_service import fetch_gp_consultation

router = APIRouter(prefix="/api/v1/diagnosis", tags=["diagnosis"])


@router.get("/{user_id}", response_model=GPConsultationSchema)
async def get_diagnosis(
    user_id: str,
    start_date: str = Query(description="ISO 8601 date (YYYY-MM-DD). Synthesise visits from this date onward."),
) -> GPConsultationSchema:
    try:
        return await fetch_gp_consultation(user_id, start_date)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
