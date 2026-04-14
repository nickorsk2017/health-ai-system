from fastmcp import Client
from loguru import logger

from config import settings


async def run_gp_synthesis(state: dict) -> dict:
    logger.info("Running GP synthesis with full patient context...")

    async with Client(settings.gp_synthesis_agent_url) as client:
        result = await client.call_tool(
            "synthesize_gp_consultation",
            {
                "data": {
                    "history_records": state.get("history_records", []),
                    "lab_records": state.get("lab_records", []),
                    "device_records": state.get("device_records", []),
                    "complaint_records": state.get("complaint_records", []),
                    "consilium_findings": state.get("consilium_findings", []),
                }
            },
        )

    consultation = result.structured_content or {}
    logger.info("GP synthesis complete.")
    return {**state, "consultation": consultation}
