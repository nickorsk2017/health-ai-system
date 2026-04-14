from fastmcp import FastMCP
from loguru import logger

from config import settings
from schemas.http import EvaluationRequest
from tools.run_comprehensive_evaluation import run_comprehensive_evaluation as _evaluate

logger.add("mcp.log", rotation="10 MB")

mcp = FastMCP("master-orchestrator-agent")


@mcp.tool(name="run_comprehensive_evaluation")
async def run_comprehensive_evaluation(data: EvaluationRequest) -> dict:
    """Orchestrate a full patient MDT evaluation.

    Fetches SOAP history and laboratory results in parallel, then runs
    a board of 9 specialist LLMs concurrently to produce multidisciplinary findings.

    Args:
        user_id: Identifier of the patient.
        start_date: ISO 8601 start date for data retrieval (YYYY-MM-DD).
    """
    result = await _evaluate(data)
    return result.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
