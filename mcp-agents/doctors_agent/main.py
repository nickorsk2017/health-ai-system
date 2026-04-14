from fastmcp import FastMCP
from loguru import logger

from config import settings
from schemas.http import ConsiliumRequest
from services.consilium_service import ConsiliumService

logger.add("mcp.log", rotation="10 MB")

mcp = FastMCP("doctors-agent")

_consilium_service = ConsiliumService()


@mcp.resource("config://specialties")
def get_specialties() -> str:
    return (
        "specialties: oncology, gastroenterology, cardiology, hematology, "
        "nephrology, nutrition, endocrinology, mental_health, pulmonology"
    )


@mcp.tool(name="run_medical_consilium")
async def run_medical_consilium(data: ConsiliumRequest) -> list[dict]:
    """Run patient history and lab data through a board of 9 specialist LLMs in parallel.

    Args:
        history_records: SOAP patient history records from client_history_agent.
        lab_records: Laboratory analysis records from labs_agent.
    """
    logger.info(
        f"Starting consilium: {len(data.history_records)} SOAP note(s), "
        f"{len(data.lab_records)} lab record(s)"
    )

    findings = await _consilium_service.run(data.history_records, data.lab_records)

    logger.info(f"Consilium finished: {len(findings)} specialist finding(s) returned.")
    return [f.model_dump() for f in findings]


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


if __name__ == "__main__":
    run()
