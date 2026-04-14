from loguru import logger

from graph.state import OrchestratorState
from graph.workflow import build_workflow
from schemas.http import EvaluationRequest, EvaluationResponse

_workflow = build_workflow()


async def run_comprehensive_evaluation(request: EvaluationRequest) -> EvaluationResponse:
    logger.info(
        f"Starting comprehensive evaluation: user={request.user_id}, from={request.start_date}"
    )

    initial_state: OrchestratorState = {
        "user_id": request.user_id,
        "start_date": str(request.start_date),
        "history_records": [],
        "lab_records": [],
        "history_error": None,
        "labs_error": None,
        "findings": [],
    }

    final_state: OrchestratorState = await _workflow.ainvoke(initial_state)

    logger.info(
        f"Evaluation complete: {len(final_state['findings'])} finding(s), "
        f"history={'ok' if not final_state['history_error'] else 'missing'}, "
        f"labs={'ok' if not final_state['labs_error'] else 'missing'}"
    )

    return EvaluationResponse(
        findings=final_state["findings"],
        history_available=not bool(final_state["history_error"]),
        labs_available=not bool(final_state["labs_error"]),
    )
