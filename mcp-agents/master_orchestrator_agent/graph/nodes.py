import asyncio

from fastmcp import Client
from loguru import logger

from config import settings
from graph.state import OrchestratorState


async def _fetch_history(user_id: str, start_date: str) -> tuple[list[dict], str | None]:
    try:
        async with Client(settings.client_history_agent_url) as client:
            result = await client.call_tool(
                "get_patient_history",
                {"data": {"user_id": user_id, "last_history_date": start_date, "doctor_type": ""}},
            )
        payload = result.structured_content or {}
        records = payload.get("result", [])
        if not isinstance(records, list):
            return [], "Unexpected history response format"
        logger.info(f"Fetched {len(records)} SOAP record(s) for user={user_id}")
        return records, None
    except Exception as exc:
        logger.error(f"History fetch failed for user={user_id}: {exc}")
        return [], str(exc)


async def _fetch_labs(user_id: str, start_date: str) -> tuple[list[dict], str | None]:
    try:
        async with Client(settings.labs_agent_url) as client:
            result = await client.call_tool(
                "get_patient_analyses",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
        payload = result.structured_content or {}
        records = payload.get("result", [])
        if not isinstance(records, list):
            return [], "Unexpected labs response format"
        logger.info(f"Fetched {len(records)} lab record(s) for user={user_id}")
        return records, None
    except Exception as exc:
        logger.error(f"Labs fetch failed for user={user_id}: {exc}")
        return [], str(exc)


async def gather_data(state: OrchestratorState) -> OrchestratorState:
    user_id = state["user_id"]
    start_date = state["start_date"]

    logger.info(f"Parallel data gathering: user={user_id}, from={start_date}")

    (history_records, history_error), (lab_records, labs_error) = await asyncio.gather(
        _fetch_history(user_id, start_date),
        _fetch_labs(user_id, start_date),
    )

    if history_error:
        logger.warning(f"Proceeding without history — {history_error}")
    if labs_error:
        logger.warning(f"Proceeding without labs — {labs_error}")

    return {
        **state,
        "history_records": history_records,
        "lab_records": lab_records,
        "history_error": history_error,
        "labs_error": labs_error,
    }


async def run_consilium(state: OrchestratorState) -> OrchestratorState:
    history_records = state["history_records"]
    lab_records = state["lab_records"]

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
    return {**state, "findings": findings}
