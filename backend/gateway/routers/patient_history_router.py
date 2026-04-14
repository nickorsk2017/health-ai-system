from fastapi import APIRouter, HTTPException, Query

from schemas.patient_history_schema import (
    CreatePatientHistorySchema,
    HistoryFromPromptRequestSchema,
    HistoryFromPromptResponseSchema,
    MutatePatientHistoryResponseSchema,
    PatientHistoryRecordSchema,
    RecordPatientHistoryResponseSchema,
    UpdatePatientHistorySchema,
)
from services.patient_history_service import (
    create_history_from_prompt,
    delete_patient_history,
    fetch_patient_history,
    record_patient_history,
    update_patient_history,
)

router = APIRouter(prefix="/api/v1/patient-history", tags=["patient-history"])


@router.post("", response_model=RecordPatientHistoryResponseSchema, status_code=201)
async def create_patient_history(body: CreatePatientHistorySchema) -> RecordPatientHistoryResponseSchema:
    agent_result = await record_patient_history(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.post("/by-prompt", response_model=HistoryFromPromptResponseSchema, status_code=201)
async def import_history_from_prompt(body: HistoryFromPromptRequestSchema) -> HistoryFromPromptResponseSchema:
    agent_result = await create_history_from_prompt(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.get("/{user_id}", response_model=list[PatientHistoryRecordSchema])
async def get_patient_history(
    user_id: str,
    last_history_date: str = Query(
        description="ISO 8601 date (YYYY-MM-DD). Returns records from this date onward."
    ),
) -> list[PatientHistoryRecordSchema]:
    agent_result = await fetch_patient_history(user_id, last_history_date)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.patch("/{history_id}", response_model=MutatePatientHistoryResponseSchema)
async def patch_patient_history(
    history_id: str, body: UpdatePatientHistorySchema
) -> MutatePatientHistoryResponseSchema:
    agent_result = await update_patient_history(history_id, body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.delete("/{history_id}", response_model=MutatePatientHistoryResponseSchema)
async def remove_patient_history(history_id: str) -> MutatePatientHistoryResponseSchema:
    agent_result = await delete_patient_history(history_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
