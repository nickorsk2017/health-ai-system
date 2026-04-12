from datetime import date

from loguru import logger
from sqlalchemy import select

from db.engine import SessionLocal
from db.models import Visit
from schemas.visit import DoctorType, DoctorVisit
from schemas.http import GetDoctorVisitsHistoryRequest


async def get_doctor_visits_history(
  data: GetDoctorVisitsHistoryRequest
) -> list[DoctorVisit]:

    logger.info(
        f"Fetching visits: user={data.user_id}, from={data.last_date_visit}, specialty={data.doctor_type if data.doctor_type else 'all'}"
    )

    query = (
        select(Visit)
        .where(Visit.user_id == data.user_id)
        .where(Visit.visit_at >= data.last_date_visit)
        .order_by(Visit.visit_at.asc())
    )

    if data.doctor_type is not None and data.doctor_type != "":
        query = query.where(Visit.doctor_type == data.doctor_type)

    async with SessionLocal() as session:
        result = await session.execute(query)
        rows = result.scalars().all()

    visits = [
        DoctorVisit(
            visit_id=str(row.id),
            user_id=row.user_id,
            doctor_type=DoctorType(row.doctor_type),
            visit_at=row.visit_at.isoformat(),
            subjective=row.subjective,
            objective=row.objective,
            assessment=row.assessment,
            plan=row.plan,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]

    logger.info(f"Found {len(visits)} visit(s)")
    return visits
