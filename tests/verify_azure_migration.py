import sys
import os
import logging
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.getcwd())

load_dotenv()

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(name)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)



from agents.policy_agent import PolicyInterpretationAgent
# from api.dependencies import get_policy_search_client # Avoid importing this directly to skip unrelated initialization errors
from agents.search.policy_search import PolicySearchClient
from contracts.agents.policy_agent_contract import PolicyAgentInput
from contracts.risk_output import RiskEvaluationOutput, RiskBand
from contracts.credit_application import CreditApplication


from dotenv import load_dotenv # Add dotenv import

# Replicating the logic from api/dependencies.py to verify it works in isolation
def get_policy_search_client_verified():
    load_dotenv() # Load env vars
    if os.getenv("USE_AZURE_SEARCH") == "true":
        print("Using Azure Search (Env var detected)")
        return PolicySearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY")
        )
    print("Using Fake Fallback")
    class FakePolicySearchClient:
        def search(self, query: str, top_k: int = 5):
            return ["FAKE RESULT"]
    return FakePolicySearchClient()

class FakeLLM:
    def generate(self, prompt: str) -> str:
        return '{"policy_status": "CONDITIONAL", "conditions": ["TEST"], "hard_stop": false, "policy_references": []}'

def main():
    # Setup logging to file
    file_handler = logging.FileHandler("verify_output_utf8.log", mode='w', encoding='utf-8')
    formatter = logging.Formatter('%(levelname)s | %(name)s | %(message)s')
    file_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    print("--- Verification with FakeLLM & Real Search (Isolated) ---")
    
    try:
        # 1. Get Real Search Client (Verified Logic)
        search_client = get_policy_search_client_verified()
        # print(f"Obtained search client: {type(search_client)}") # Print goes to stdout, let's allow it
        
        # 2. Setup Agent
        agent = PolicyInterpretationAgent(
            llm=FakeLLM(),
            search_client=search_client,
            prompt_template="Test Prompt"
        )
        
        # 3. Create Input
        app = CreditApplication(
            application_id="APP-TEST",
            applicant_id="CUST-TEST",
            employment_type="SALARIED",
            monthly_income=50000,
            existing_emi=10000,
            credit_score=650,
            loan_amount=200000,
            loan_tenure_months=24,
            product_type="PERSONAL_LOAN",
            channel="DIGITAL",
            declared_assets_value=50000 # Fixed > 0
        )
        risk = RiskEvaluationOutput(risk_band=RiskBand.MEDIUM, risk_factors=[], data_quality_issues=[])
        
        # 4. Run Agent
        print("Running agent...")
        agent.run(PolicyAgentInput(application=app, risk_output=risk))
        print("Agent run complete. Checking logs...")
        
    except Exception as e:
        print(f"FAILED: {e}")
        logging.error(f"FAILED: {e}")

if __name__ == "__main__":
    main()
