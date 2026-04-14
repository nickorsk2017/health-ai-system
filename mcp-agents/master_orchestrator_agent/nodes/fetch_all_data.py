import asyncio

from fastmcp import Client
from loguru import logger

from config import settings
from schemas.state import ConsiliumState, GPDiagnosisState


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


async def _fetch_devices(user_id: str) -> tuple[list[dict], str | None]:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            result = await client.call_tool(
                "get_patient_devices",
                {"user_id": user_id},
            )
        payload = result.structured_content or {}
        records = payload.get("result", [])
        if not isinstance(records, list):
            return [], "Unexpected device response format"
        logger.info(f"Fetched {len(records)} device record(s) for user={user_id}")
        return records, None
    except Exception as exc:
        logger.error(f"Devices fetch failed for user={user_id}: {exc}")
        return [], str(exc)


async def _fetch_complaints(user_id: str) -> tuple[list[dict], str | None]:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            result = await client.call_tool(
                "get_complaints",
                {"data": {"user_id": user_id}},
            )
        payload = result.structured_content or {}
        records = payload.get("result", [])
        if not isinstance(records, list):
            return [], "Unexpected complaints response format"
        logger.info(f"Fetched {len(records)} complaint record(s) for user={user_id}")
        return records, None
    except Exception as exc:
        logger.error(f"Complaints fetch failed for user={user_id}: {exc}")
        return [], str(exc)


async def fetch_history_labs(state: ConsiliumState) -> ConsiliumState:
    user_id = state["user_id"]
    start_date = state["start_date"]

    logger.info(f"Parallel fetch (history + labs): user={user_id}, from={start_date}")

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


async def fetch_all_data(state: GPDiagnosisState) -> GPDiagnosisState:
    user_id = state["user_id"]
    start_date = state["start_date"]

    logger.info(f"Parallel fetch (all sources): user={user_id}, from={start_date}")

    results = await asyncio.gather(
        _fetch_history(user_id, start_date),
        _fetch_labs(user_id, start_date),
        _fetch_devices(user_id),
        _fetch_complaints(user_id),
    )

    (history_records, history_error) = results[0]
    (lab_records, labs_error) = results[1]
    (device_records, devices_error) = results[2]
    (complaint_records, complaints_error) = results[3]

    for label, err in (
        ("history", history_error),
        ("labs", labs_error),
        ("devices", devices_error),
        ("complaints", complaints_error),
    ):
        if err:
            logger.warning(f"Proceeding without {label} — {err}")

    return {
        **state,
        "history_records": history_records,
        "lab_records": lab_records,
        "device_records": device_records,
        "complaint_records": complaint_records,
        "history_error": history_error,
        "labs_error": labs_error,
        "devices_error": devices_error,
        "complaints_error": complaints_error,
    }
