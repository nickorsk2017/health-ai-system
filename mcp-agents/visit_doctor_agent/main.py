from contextlib import asynccontextmanager
from datetime import date
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from db.init import create_tables
from schemas.visit import  DoctorVisit
from schemas.http import GetDoctorVisitsHistoryRequest
from tools.get_doctor_visits_history import get_doctor_visits_history as _get_history
from tools.add_visit_doctor import add_visit_doctor as _record_visit


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Initialising database tables...")
    await create_tables()
    logger.info("Database ready.")
    yield


mcp = FastMCP("visit-doctor-mcp-agent", lifespan=lifespan)


@mcp.resource("config://schema")
def get_schema() -> str:
    return (
        "table: visits\n"
        "columns: id (uuid), user_id, doctor_type, visit_at, "
        "subjective, objective, assessment, plan, created_at"
    )


@mcp.tool(name="add_visit_doctor")
async def add_visit_doctor(data: DoctorVisit) -> dict:
    """Record a new specialist consultation in SOAP format.

    Args:
        doctor_type: Medical specialty (oncology, gastroenterology, cardiology,
            hematology, nephrology, nutrition, endocrinology, mental_health, pulmonology).
        subjective: Patient complaints, history, and symptoms as reported.
        objective: Clinical findings, vitals, and examination results.
        assessment: Clinical impression or diagnosis.
        visit_at: ISO 8601 date of the consultation (YYYY-MM-DD).
        user_id: Identifier of the patient.
        plan: Treatment plan or next steps (optional).
    """
    result = await _record_visit(data)
    return result.model_dump()


@mcp.tool(name="get_doctor_visits_history")
async def get_doctor_visits_history(
    data: GetDoctorVisitsHistoryRequest
) -> list[DoctorVisit]:
    """Retrieve SOAP notes for a user from a given date to today.

    Args:
        last_date_visit: ISO 8601 start date for the search (YYYY-MM-DD).
        user_id: Identifier of the patient.
        doctor_type: Optional specialty filter (oncology, gastroenterology, cardiology,
            hematology, nephrology, nutrition, endocrinology, mental_health, pulmonology).
    """
    records = await _get_history(data)
    return [r.model_dump() for r in records]


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
