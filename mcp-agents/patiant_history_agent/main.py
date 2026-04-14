from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from config import settings
from db.init import create_tables
from schemas.patient_history import PatientHistoryRecord
from schemas.http import (
    CreateHistoryFromPromptRequest,
    DeletePatientHistoryRequest,
    GetPatientHistoryRequest,
    UpdatePatientHistoryRequest,
)
from tools.add_patient_history import add_patient_history as _record_history
from tools.create_history_from_prompt import create_history_from_prompt as _create_from_prompt
from tools.delete_patient_history import delete_patient_history as _delete_history
from tools.get_patient_history import get_patient_history as _get_history
from tools.update_patient_history import update_patient_history as _update_history

logger.add("mcp.log", rotation="10 MB")


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Initialising database tables...")
    await create_tables()
    logger.info("Database ready.")
    yield


mcp = FastMCP("client-history-agent", lifespan=lifespan)


@mcp.resource("config://schema")
def get_schema() -> str:
    return (
        "table: patient_histories\n"
        "columns: id (uuid), user_id, doctor_type, history_date, "
        "subjective, objective, assessment, plan, created_at"
    )


@mcp.tool(name="add_patient_history")
async def add_patient_history(data: PatientHistoryRecord) -> dict:
    """Record a new specialist consultation in SOAP format.

    Args:
        doctor_type: Medical specialty (oncology, gastroenterology, cardiology,
            hematology, nephrology, nutrition, endocrinology, mental_health, pulmonology).
        subjective: Patient complaints, history, and symptoms as reported.
        objective: Clinical findings, vitals, and examination results.
        assessment: Clinical impression or diagnosis.
        history_date: ISO 8601 date of the consultation (YYYY-MM-DD).
        user_id: Identifier of the patient.
        plan: Treatment plan or next steps (optional).
    """
    result = await _record_history(data)
    return result.model_dump()


@mcp.tool(name="get_patient_history")
async def get_patient_history(data: GetPatientHistoryRequest) -> list[PatientHistoryRecord]:
    """Retrieve SOAP notes for a user from a given date to today.

    Args:
        last_history_date: ISO 8601 start date for the search (YYYY-MM-DD).
        user_id: Identifier of the patient.
        doctor_type: Optional specialty filter (oncology, gastroenterology, cardiology,
            hematology, nephrology, nutrition, endocrinology, mental_health, pulmonology).
    """
    records = await _get_history(data)
    return [r.model_dump() for r in records]


@mcp.tool(name="create_history_from_prompt")
async def create_history_from_prompt(data: CreateHistoryFromPromptRequest) -> dict:
    """Parse a natural language prompt and batch-create multiple SOAP patient history records.

    Args:
        user_id: Identifier of the patient.
        prompt: Free-text clinical notes describing one or more medical visits. May include
            dates, specialist types, symptoms, findings, diagnoses, and treatment plans.
            Multiple visits on different dates are supported in a single prompt.
    """
    result = await _create_from_prompt(data)
    return result.model_dump()


@mcp.tool(name="update_patient_history")
async def update_patient_history(data: UpdatePatientHistoryRequest) -> dict:
    """Update an existing SOAP patient history record.

    Args:
        history_id: UUID of the patient history record to update.
        history_date: ISO 8601 date of the consultation (YYYY-MM-DD).
        subjective: Patient complaints, history, and symptoms.
        objective: Clinical findings, vitals, and examination results.
        assessment: Clinical impression or diagnosis.
        plan: Treatment plan or next steps.
    """
    result = await _update_history(data)
    return result.model_dump()


@mcp.tool(name="delete_patient_history")
async def delete_patient_history(data: DeletePatientHistoryRequest) -> dict:
    """Permanently delete a patient history record by its ID.

    Args:
        history_id: UUID of the patient history record to delete.
    """
    result = await _delete_history(data)
    return result.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
