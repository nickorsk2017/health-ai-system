from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Patient
from schemas.patient_schema import CreatePatientSchema


async def create_patient(session: AsyncSession, data: CreatePatientSchema) -> Patient:
    patient = Patient(
        full_name=data.full_name,
        dob=data.dob,
        gender=data.gender,
    )
    session.add(patient)
    await session.commit()
    await session.refresh(patient)
    return patient


async def list_patients(session: AsyncSession) -> list[Patient]:
    result = await session.execute(select(Patient).order_by(Patient.created_at))
    return list(result.scalars().all())
