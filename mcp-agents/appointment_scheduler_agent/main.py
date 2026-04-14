from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from config import settings
from db.init import create_tables
from schemas.appointment import CreateAppointmentRequest, GetAppointmentsRequest
from tools.create_appointment import create_appointment as _create_appointment
from tools.get_appointments import get_appointments as _get_appointments

logger.add("mcp.log", rotation="10 MB")


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Initialising database tables...")
    await create_tables()
    yield


mcp = FastMCP("appointment-scheduler-agent", lifespan=lifespan)


@mcp.tool(name="create_appointment")
async def create_appointment(data: CreateAppointmentRequest) -> dict:
    """Schedule an appointment for a patient complaint. Automatically marks the complaint as 'appointment'.

    Args:
        complaint_id: UUID of the complaint this appointment addresses.
        appointment_date: ISO datetime for the appointment (YYYY-MM-DDTHH:MM:SS).
        doctor_type: Type of doctor (e.g. 'Cardiologist', 'GP', 'Endocrinologist').
        problem_notes: Optional notes about the appointment context.
    """
    result = await _create_appointment(data)
    return result.model_dump()


@mcp.tool(name="get_appointments")
async def get_appointments(data: GetAppointmentsRequest) -> list[dict]:
    """Retrieve appointments, optionally filtered by patient.

    Args:
        user_id: Filter appointments to a specific patient. Leave empty to fetch all (doctor view).
    """
    records = await _get_appointments(data)
    return [r.model_dump() for r in records]


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()
