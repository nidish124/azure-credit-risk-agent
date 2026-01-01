from fastapi import APIRouter, HTTPException
from contracts.credit_application import CreditApplication
from contracts.graph_state import CreditDecisionGraphState
from graph.builder import build_credit_decision_graph
from api.logging import setup_logger
from api.error_handler import handle_agent_error
import os
import json
from dotenv import load_dotenv
load_dotenv(override=True)
router = APIRouter()
logger = setup_logger()

@router.post("/credit/evaluate")
def evaluate_credit(app: CreditApplication):
    logger.info(
        f"Received credit evaluation request | application_id={app.application_id}"
    )
    try:
        logger.info(
            f"USING AZURE DEPLOYMENT: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}, {os.getenv('AZURE_OPENAI_API_VERSION')}"
        )
        graph = build_credit_decision_graph()
        final_state = graph.invoke(
            CreditDecisionGraphState(application=app)
        )
        cost_data = {
                "total_cost": final_state["token_tracker"].total_cost(),
                "per_agent_cost": final_state["token_tracker"].per_agent_cost(),
                "currency": "USD",
            }
        logger.info(
            "request_cost_summary: %s",json.dumps(cost_data))

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