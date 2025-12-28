from fastapi import HTTPException
import logging

logger = logging.getLogger("credit_decision")

class AgentExecutionError(Exception):
    pass

def handle_agent_error(exc: Exception):
    logger.exception(f"Agent execution failed: {str(exc)}")

    raise HTTPException(
        status_code=500,
        detail="Internal decisioning error. Please retry or escalate."
    )