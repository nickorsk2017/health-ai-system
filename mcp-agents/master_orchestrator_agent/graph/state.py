from typing import TypedDict


class OrchestratorState(TypedDict):
    user_id: str
    start_date: str
    history_records: list[dict]
    lab_records: list[dict]
    history_error: str | None
    labs_error: str | None
    findings: list[dict]
