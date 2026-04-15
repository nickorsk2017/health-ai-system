from datetime import timezone

from loguru import logger

from chains.consilium_chain import build_consilium_chain
from schemas.http import EvaluationRequest, EvaluationResponse
from schemas.state import ConsiliumState

_chain = build_consilium_chain()


async def run_comprehensive_evaluation(request: EvaluationRequest) -> EvaluationResponse:
    logger.info(
        f"Starting comprehensive evaluation: user={request.user_id}, from={request.start_date}"
    )

    start_date = request.start_date
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    else:
        start_date = start_date.astimezone(timezone.utc)
    initial_state: ConsiliumState = {
        "user_id": request.user_id,
        "start_date": start_date.isoformat(),
        "history_records": [],
        "lab_records": [],
        "history_error": None,
        "labs_error": None,
        "consilium_findings": [],
    }

    final_state: ConsiliumState = await _chain.ainvoke(initial_state)

    logger.info(
        f"Evaluation complete: {len(final_state['consilium_findings'])} finding(s), "
        f"history={'ok' if not final_state['history_error'] else 'missing'}, "
        f"labs={'ok' if not final_state['labs_error'] else 'missing'}"
    )

    return EvaluationResponse(
        findings=final_state["consilium_findings"],
        history_available=not bool(final_state["history_error"]),
        labs_available=not bool(final_state["labs_error"]),
    )
