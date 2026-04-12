import uuid
from datetime import date

from loguru import logger
from sqlalchemy import insert

from db.engine import SessionLocal
from db.models import Visit
from schemas.http import RecordDoctorVisitResponse
from schemas.visit import DoctorVisit    


async def add_visit_doctor(data: DoctorVisit) -> RecordDoctorVisitResponse:
    visit_id = uuid.uuid4()

    logger.info(f"Recording visit: user={data.user_id}, specialty={data.doctor_type.value}, date={data.date_visit}")

    async with SessionLocal() as session:
        await session.execute(
            insert(Visit).values(
                id=visit_id,
                user_id=data.user_id,
                doctor_type=data.doctor_type.value,
                date_visit=data.date_visit,
                subjective=data.subjective,
                objective=data.objective,
                assessment=data.assessment,
                plan=data.plan,
            )
        )
        await session.commit()

    logger.info(f"Visit recorded: visit_id={visit_id}")
    return RecordDoctorVisitResponse(success=True, visit_id=str(visit_id))
