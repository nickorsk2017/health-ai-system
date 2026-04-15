from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from schemas.diagnosis_schema import GPConsultationSchema
from services.gp_service import fetch_gp_consultation

router = APIRouter(prefix="/api/v1/diagnosis", tags=["diagnosis"])


@router.get("/{user_id}", response_model=GPConsultationSchema)
async def get_diagnosis(
    user_id: str,
    start_date: datetime = Query(description="ISO 8601 UTC datetime. Synthesise visits from this timestamp onward."),
) -> GPConsultationSchema:
    agent_result = await fetch_gp_consultation(user_id, start_date)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
