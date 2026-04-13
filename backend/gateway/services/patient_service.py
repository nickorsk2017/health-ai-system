import httpx

from config import settings
from schemas.patient_schema import CreatePatientSchema, PatientSchema
from services.exceptions import AgentConnectionError, NoDataFoundError


async def list_patients() -> list[PatientSchema]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.user_service_url}/patients")
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise AgentConnectionError(f"user_microservice unreachable: {exc}") from exc

    data = response.json()
    if not isinstance(data, list):
        raise NoDataFoundError("user_microservice returned unexpected response")

    return [PatientSchema(**p) for p in data]


async def create_patient(data: CreatePatientSchema) -> PatientSchema:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.user_service_url}/patients",
                json=data.model_dump(mode="json"),
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise AgentConnectionError(f"user_microservice unreachable: {exc}") from exc

    return PatientSchema(**response.json())
