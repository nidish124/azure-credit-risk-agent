from contracts.graph_state import CreditDecisionGraphState


def policy_hard_stop(state: CreditDecisionGraphState) -> str:
    if state.policy_output and state.policy_output.hard_stop:
        return "decision"
    return "explain"
