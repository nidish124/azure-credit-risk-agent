from contracts.agents.risk_agent_contract import RiskAgentInput
from contracts.credit_application import CreditApplication
from agents.risk_agent import RiskScoringAgent
from agents.ollama_provider import OllamaProvider
import os
from dotenv import load_dotenv
from api.factories import FakeLLM

load_dotenv()

def test_risk_agent_input_contract():
    app = CreditApplication(
        application_id="app-10",
        applicant_id="cust-10",
        employment_type="SALARIED",
        monthly_income=90000,
        existing_emi=30000,
        credit_score=730,
        loan_amount=600000,
        loan_tenure_months=36,
        product_type="PERSONAL_LOAN",
        channel="DIGITAL",
        declared_assets_value=800000
    )

    execution = os.getenv("EXECUTION_MODE")


    curr_llm = OllamaProvider()
    
    if execution == "ci":
        curr_llm = FakeLLM()
    

    agent = RiskScoringAgent(
        llm=curr_llm,
        prompt_template=open("agents/prompts/risk_prompt.txt").read()
    )

    output = agent.run(RiskAgentInput(application=app))

    inp = RiskAgentInput(application=app)
    assert inp.application.loan_amount == 600000

    assert output.risk_band in ["LOW", "MEDIUM", "HIGH"]
    assert len(output.risk_factors) > 0