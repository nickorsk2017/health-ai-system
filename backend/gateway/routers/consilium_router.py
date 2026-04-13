from fastapi import APIRouter, HTTPException, Query

from schemas.consilium_schema import SpecialistFindingSchema
from services.consilium_service import fetch_consilium
from services.exceptions import AgentConnectionError, NoDataFoundError

router = APIRouter(prefix="/api/v1/consilium", tags=["consilium"])


@router.get("/{user_id}", response_model=list[SpecialistFindingSchema])
async def get_consilium(
    user_id: str,
    start_date: str = Query(description="ISO 8601 date (YYYY-MM-DD). Analyse visits from this date onward."),
) -> list[SpecialistFindingSchema]:
    try:
        return await fetch_consilium(user_id, start_date)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
