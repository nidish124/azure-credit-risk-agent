from agents.policy_agent import PolicyInterpretationAgent
from contracts.credit_application import CreditApplication
from contracts.agents.policy_agent_contract import PolicyAgentInput
from contracts.risk_output import RiskEvaluationOutput, RiskBand


class FakePolicySearchClient:
    def search(self, query: str, top_k: int = 5):
        return [
            "CREDIT-POL-4.2: Applicants with credit score below 720 require a guarantor."
        ]

class FakeLLM:
    def generate(self, prompt: str) -> str:
        return """
        {
          "policy_status": "CONDITIONAL",
          "conditions": ["ADD_GUARANTOR"],
          "hard_stop": false,
          "policy_references": ["CREDIT-POL-4.2"]
        }
        """


def test_policy_agent_runs():
    app = CreditApplication(
        application_id="APP-POL-1",
        applicant_id="CUST-POL",
        employment_type="SALARIED",
        monthly_income=90000,
        existing_emi=30000,
        credit_score=710,
        loan_amount=600000,
        loan_tenure_months=36,
        product_type="PERSONAL_LOAN",
        channel="DIGITAL",
        declared_assets_value=800000
    )

    risk = RiskEvaluationOutput(
        risk_band=RiskBand.MEDIUM,
        risk_factors=[],
        data_quality_issues=[]
    )

    agent = PolicyInterpretationAgent(
        llm=FakeLLM(),
        search_client=FakePolicySearchClient(),
        prompt_template=open("agents/prompts/policy_prompt.txt").read()
    )

    output = agent.run(PolicyAgentInput(application=app, risk_output=risk))

    assert output.policy_status == "CONDITIONAL"
    assert "ADD_GUARANTOR" in output.conditions
