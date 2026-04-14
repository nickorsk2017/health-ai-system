from db.engine import Base, engine
from db.models import Appointment  # noqa: F401 — registers model with metadata


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
