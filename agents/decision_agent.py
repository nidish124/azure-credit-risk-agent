from contracts.agents.decision_agent_contract import (
    DecisionAgentInput,
    DecisionAgentOutput
)
from contracts.decision_output import DecisionRecommendation


class DecisionSynthesisAgent:
    def run(self, inp: DecisionAgentInput) -> DecisionAgentOutput:
        policy = inp.policy_output
        risk = inp.risk_output

        # Rule 1: Hard stop
        if policy.hard_stop:
            return DecisionAgentOutput(
                recommendation=DecisionRecommendation.REJECT,
                required_actions=[],
                confidence=0.95
            )

        # Rule 2: Policy fail (no hard stop)
        if policy.policy_status == "FAIL":
            return DecisionAgentOutput(
                recommendation=DecisionRecommendation.MANUAL_REVIEW,
                required_actions=[],
                confidence=0.6
            )

        # Rule 3: Conditional policy
        if policy.policy_status == "CONDITIONAL":
            return DecisionAgentOutput(
                recommendation=DecisionRecommendation.CONDITIONAL_APPROVE,
                required_actions=policy.conditions,
                confidence=0.75
            )

        # Rule 4: Policy pass + low risk
        if policy.policy_status == "PASS" and risk.risk_band == "LOW":
            return DecisionAgentOutput(
                recommendation=DecisionRecommendation.APPROVE,
                required_actions=[],
                confidence=0.85
            )

        # Rule 5 & 6: Medium or high risk
        return DecisionAgentOutput(
            recommendation=DecisionRecommendation.MANUAL_REVIEW,
            required_actions=[],
            confidence=0.65
        )
