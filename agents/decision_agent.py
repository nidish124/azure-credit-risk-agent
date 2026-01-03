from contracts.agents.decision_agent_contract import (
    DecisionAgentInput,
    DecisionAgentOutput
)
from contracts.decision_output import DecisionRecommendation

class DecisionSynthesisAgent:
    def __init__(self):
        pass

    def _compute_dti(self, monthly_income: int, existing_emi: int) -> float:
        """Calculates Debt-to-Income ratio."""
        if monthly_income == 0:
            return 0.0
        return round(existing_emi / monthly_income, 2)

    def _compute_confidence(self, 
        credit_score: int,
        dti: float,
        risk_band: str,
        hard_stop: bool,
        num_conditions: int
        ) -> float:
        confidence = 0.90  # baseline approval confidence

        # Credit score impact
        if credit_score < 700:
            confidence -= 0.15
        elif credit_score < 750:
            confidence -= 0.08

        # DTI impact
        if dti > 0.5:
            confidence -= 0.15
        elif dti > 0.4:
            confidence -= 0.08

        # Risk band impact
        if risk_band == "MEDIUM":
            confidence -= 0.10
        elif risk_band == "HIGH":
            confidence -= 0.25

        # Policy conditions impact
        confidence -= min(num_conditions * 0.05, 0.20)

        # Hard stop means very low confidence
        if hard_stop:
            confidence = min(confidence, 0.30)

        # Clamp
        return round(max(0.05, min(confidence, 0.95)), 2)

    def run(self, inp: DecisionAgentInput) -> DecisionAgentOutput:
        policy = inp.policy_output
        risk = inp.risk_output
        application = inp.application

        # Rule 1: Hard stop
        if policy.hard_stop:
            recommendation = DecisionRecommendation.REJECT
            required_actions = []
        
        # Rule 2: Policy fail (no hard stop)
        elif policy.policy_status == "FAIL":
            recommendation = DecisionRecommendation.MANUAL_REVIEW
            required_actions = []
        
        # Rule 3: Conditional policy
        elif policy.policy_status == "CONDITIONAL":
            recommendation = DecisionRecommendation.CONDITIONAL_APPROVE
            required_actions = policy.conditions
        
        # Rule 4: Policy pass + low risk
        elif policy.policy_status == "PASS" and risk.risk_band == "LOW":
            recommendation = DecisionRecommendation.APPROVE
            required_actions = []
        
        # Rule 5 & 6: Policy pass but medium/high risk, or uncaught
        else: 
            recommendation = DecisionRecommendation.MANUAL_REVIEW
            required_actions = []

        dti = self._compute_dti(
            monthly_income=application.monthly_income,
            existing_emi=application.existing_emi
        )

        num_conditions = len(policy.conditions)

        confidence = self._compute_confidence(
            credit_score=application.credit_score,
            dti = dti,
            risk_band = risk.risk_band,
            hard_stop=policy.hard_stop,
            num_conditions=num_conditions
        )

        return DecisionAgentOutput(
            recommendation=recommendation,
            required_actions=required_actions,
            confidence=confidence,
            max_eligibility_loan_amount = risk.max_eligibility_loan_amount
        )
