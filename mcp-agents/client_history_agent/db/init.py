from sqlalchemy import text

from db.engine import engine
from db.models import Base


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'visits') THEN
                    ALTER TABLE visits RENAME TO patient_histories;
                END IF;
            END;
            $$;
        """))
        await conn.execute(text("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'patient_histories' AND column_name = 'visit_at'
                ) THEN
                    ALTER TABLE patient_histories RENAME COLUMN visit_at TO history_date;
                END IF;
            END;
            $$;
        """))
