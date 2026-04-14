from fastmcp import Client
from loguru import logger

from config import settings


async def run_consilium(state: dict) -> dict:
    history_records = state.get("history_records", [])
    lab_records = state.get("lab_records", [])

    if not history_records and not lab_records:
        raise ValueError(
            f"No patient data available for consilium "
            f"(history_error={state.get('history_error')!r}, "
            f"labs_error={state.get('labs_error')!r})"
        )

    logger.info(
        f"Running consilium: {len(history_records)} SOAP note(s), "
        f"{len(lab_records)} lab record(s)"
    )

    async with Client(settings.doctors_agent_url) as client:
        result = await client.call_tool(
            "run_medical_consilium",
            {
                "data": {
                    "history_records": history_records,
                    "lab_records": lab_records,
                }
            },
        )

    payload = result.structured_content or {}
    findings = payload.get("result", [])
    if not isinstance(findings, list):
        findings = []

    logger.info(f"Consilium returned {len(findings)} finding(s)")
    return {**state, "consilium_findings": findings}
