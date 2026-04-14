from typing import Any, TypedDict


class AgentResult(TypedDict):
    success: bool
    data: Any  # Pydantic schema instance, list of instances, or None on failure
    error: str | None


def to_response(data: Any = None, error: str | None = None, success: bool | None = None) -> AgentResult:
    is_success = success if success is not None else (error is None)
    return {"success": is_success, "data": data, "error": error}
