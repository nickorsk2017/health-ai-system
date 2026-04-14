from fastmcp import FastMCP
from loguru import logger

from config import settings
from schemas.http import SynthesisRequest
from services.synthesis_service import SynthesisService

logger.add("mcp.log", rotation="10 MB")
mcp = FastMCP("gp-synthesis-agent")

_synthesis_service = SynthesisService()


@mcp.resource("config://model")
def get_model() -> str:
    return f"synthesis_model: {settings.openai_model}"


@mcp.tool(name="synthesize_gp_consultation")
async def synthesize_gp_consultation(data: SynthesisRequest) -> dict:
    """Synthesize a final GP consultation from pre-fetched multi-source patient context.

    Accepts the full clinical picture — specialist consilium findings, SOAP history,
    laboratory results, device data, and patient complaints — and produces a unified
    GP diagnosis, treatment plan, prognosis, and patient-facing health narrative.

    Args:
        history_records: SOAP patient history records.
        lab_records: Laboratory analysis records.
        device_records: Device and wearable data records.
        complaint_records: Patient complaint records.
        consilium_findings: Specialist findings from the MDT consilium.
    """
    logger.info(
        f"GP synthesis requested: {len(data.consilium_findings)} finding(s), "
        f"{len(data.history_records)} history record(s)"
    )

    if not data.consilium_findings:
        logger.warning("No consilium findings — returning advisory response.")
        return {
            "diagnosis": "Insufficient specialist data to establish a unifying diagnosis.",
            "treatment": (
                "Additional specialist consultations and targeted investigations are required "
                "before a treatment plan can be formulated."
            ),
            "prognosis": "Prognosis cannot be assessed without a confirmed diagnosis.",
            "summary": (
                "The medical board reviewed the available clinical data but was unable to identify "
                "a sufficient number of specialist findings to provide a responsible and accurate "
                "consultation. This may be because no visits have been recorded yet, or the history "
                "covers too short a period. Please ensure specialist visits have been recorded in the "
                "system and try again with an earlier start date."
            ),
        }

    consultation = await _synthesis_service.synthesize(
        history_records=data.history_records,
        lab_records=data.lab_records,
        device_records=data.device_records,
        complaint_records=data.complaint_records,
        consilium_findings=data.consilium_findings,
    )

    logger.info("GP consultation complete.")
    return consultation.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
