from fastapi import APIRouter, HTTPException
from contracts.credit_application import CreditApplication
from contracts.graph_state import CreditDecisionGraphState
from graph.builder import build_credit_decision_graph
from api.logging import setup_logger
from api.error_handler import handle_agent_error

router = APIRouter()
logger = setup_logger()

@router.post("/credit/evaluate")
def evaluate_credit(app: CreditApplication):
    logger.info(
        f"Received credit evaluation request | application_id={app.application_id}"
    )
    try:
        graph = build_credit_decision_graph()
        final_state = graph.invoke(
            CreditDecisionGraphState(application=app)
        )

        logger.info(
            f"Decision completed | application_id={app.application_id} "
            f"| recommendation={final_state['decision_output'].recommendation}"
        )

        return {
            "decision": final_state["decision_output"],
            "explanation": final_state.get("explanation_output")  # May be None if hard_stop
        }
    except Exception as e:
        handle_agent_error(e)