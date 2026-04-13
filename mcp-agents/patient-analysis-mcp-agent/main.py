import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from config import settings
from db.init import create_tables
from schemas.analysis import PatientAnalysis
from schemas.http import GetPatientAnalysesRequest
from tools.add_patient_analysis import add_patient_analysis as _add_analysis
from tools.get_patient_analyses import get_patient_analyses as _get_analyses

logger.remove()
logger.add(sys.stderr, level="INFO")


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Initialising database tables...")
    await create_tables()
    logger.info("Database ready.")
    yield


mcp = FastMCP("patient-analysis-mcp-agent", lifespan=lifespan)


@mcp.resource("config://schema")
def get_schema() -> str:
    return (
        "table: patient_analyses\n"
        "columns: id (uuid), user_id, analysis_text, analysis_date, created_at"
    )


@mcp.tool(name="add_patient_analysis")
async def add_patient_analysis(data: PatientAnalysis) -> dict:
    """Record a new laboratory test result for a patient.

    Args:
        user_id: Identifier of the patient.
        analysis: Raw or structured text of the lab results,
            e.g. 'Glucose: 105 mg/dL, HbA1c: 5.7%'.
        date: ISO 8601 date of the lab result (YYYY-MM-DD). Must be today or in the past.
    """
    result = await _add_analysis(data)
    return result.model_dump()


@mcp.tool(name="get_patient_analyses")
async def get_patient_analyses(data: GetPatientAnalysesRequest) -> list[dict]:
    """Retrieve laboratory test results for a patient from a given date to today.

    Args:
        user_id: Identifier of the patient.
        start_date: ISO 8601 start date for the search (YYYY-MM-DD).
    """
    records = await _get_analyses(data)
    return [r.model_dump() for r in records]


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
