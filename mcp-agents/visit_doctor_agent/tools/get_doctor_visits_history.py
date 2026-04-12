from datetime import date

from loguru import logger
from sqlalchemy import select

from db.engine import SessionLocal
from db.models import Visit
from schemas.visit import DoctorType, DoctorVisit


async def get_doctor_visits_history(
    last_date_visit: str,
    user_id: str,
    doctor_type: DoctorType | None = None,
) -> list[DoctorVisit]:
    from_date = date.fromisoformat(last_date_visit)

    logger.info(
        f"Fetching visits: user={user_id}, from={from_date}, specialty={doctor_type.value if doctor_type else 'all'}"
    )

    query = (
        select(Visit)
        .where(Visit.user_id == user_id)
        .where(Visit.date_visit >= from_date)
        .order_by(Visit.date_visit.asc())
    )

    if doctor_type is not None:
        query = query.where(Visit.doctor_type == doctor_type.value)

    async with SessionLocal() as session:
        result = await session.execute(query)
        rows = result.scalars().all()

    visits = [
        DoctorVisit(
            visit_id=str(row.id),
            user_id=row.user_id,
            doctor_type=DoctorType(row.doctor_type),
            date_visit=row.date_visit.isoformat(),
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
