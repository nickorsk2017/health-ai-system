from fastapi import APIRouter, HTTPException, Query

from schemas.complaint_schema import UpsertComplaintSchema, ComplaintRecordSchema
from services.complaint_service import (
    fetch_complaints,
    mark_complaint_read,
    remove_complaint,
    upsert_complaint,
)

router = APIRouter(prefix="/api/v1/complaints", tags=["complaints"])


@router.post("", status_code=201)
async def add_complaint(body: UpsertComplaintSchema) -> None:
    agent_result = await upsert_complaint(None, body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])


@router.get("", response_model=list[ComplaintRecordSchema])
async def list_complaints(user_id: str = Query(default="")) -> list[ComplaintRecordSchema]:
    agent_result = await fetch_complaints(user_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.patch("/{complaint_id}", status_code=204)
async def edit_complaint(complaint_id: str, body: UpsertComplaintSchema) -> None:
    agent_result = await upsert_complaint(complaint_id, body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])


@router.patch("/{complaint_id}/read", status_code=204)
async def read_complaint(complaint_id: str) -> None:
    agent_result = await mark_complaint_read(complaint_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])


@router.delete("/{complaint_id}", status_code=204)
async def delete_complaint(complaint_id: str) -> None:
    agent_result = await remove_complaint(complaint_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
