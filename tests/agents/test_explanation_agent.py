from agents.explanation_agent import ExplainabilityAgent
from contracts.agents.explanation_agent_contract import ExplanationAgentInput
from contracts.risk_output import RiskEvaluationOutput, RiskBand
from contracts.policy_output import PolicyEvaluationOutput, PolicyStatus


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return """
        {
          "summary": "Application shows moderate risk due to debt obligations.",
          "key_reasons": [
            "High debt-to-income ratio",
            "Guarantor required as per policy"
          ],
          "risk_references": ["DEBT_TO_INCOME"],
          "policy_references": ["CREDIT-POL-4.2"]
        }
        """


def test_explanation_agent_runs():
    risk = RiskEvaluationOutput(
        risk_band=RiskBand.MEDIUM,
        risk_factors=[
            {"factor": "DEBT_TO_INCOME", "impact": "HIGH"}
        ],
        data_quality_issues=[]
    )

    policy = PolicyEvaluationOutput(
        policy_status=PolicyStatus.CONDITIONAL,
        conditions=["ADD_GUARANTOR"],
        hard_stop=False,
        policy_references=["CREDIT-POL-4.2"]
    )

    agent = ExplainabilityAgent(
        llm=FakeLLM(),
        prompt_template=open("agents/prompts/explanation_prompt.txt").read()
    )

    output = agent.run(
        ExplanationAgentInput(
            risk_output=risk,
            policy_output=policy
        )
    )

    assert "DEBT_TO_INCOME" in output.risk_references
    assert "CREDIT-POL-4.2" in output.policy_references