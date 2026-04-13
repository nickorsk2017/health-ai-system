from fastapi import APIRouter, HTTPException

from schemas.patient_schema import CreatePatientSchema, PatientSchema
from services.exceptions import AgentConnectionError
from services.patient_service import create_patient, list_patients

router = APIRouter(prefix="/api/v1/patients", tags=["patients"])


@router.get("", response_model=list[PatientSchema])
async def get_patients() -> list[PatientSchema]:
    try:
        return await list_patients()
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.post("", response_model=PatientSchema, status_code=201)
async def add_patient(body: CreatePatientSchema) -> PatientSchema:
    try:
        return await create_patient(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
