import os
from dotenv import load_dotenv
from agents.ollama_provider import OllamaProvider
from agents.azure_openai_provider import AzureOpenAIProvider
from agents.search.policy_search import PolicySearchClient
import json

load_dotenv()

class FakeLLM:
    def generate(self, prompt: str) -> str:
        # Risk Agent
        if "Applicant Data:" in prompt:
            return json.dumps({
                "risk_band": "MEDIUM",
                "risk_factors": [
                    {"factor": "Credit Score", "impact": "HIGH"}
                ],
                "data_quality_issues": []
            })
        
        # Explanation Agent
        if "Risk output:" in prompt or "Policy Output:" in prompt:
            return json.dumps({
                "summary": "Application requires manual review due to medium risk.",
                "key_reasons": ["Credit score is below 720", "Loan to income ratio"],
                "risk_references": ["Credit Score"],
                "policy_references": ["CREDIT-POL-4.2"]
            })

        # Policy Agent (Default or specific check)
        return json.dumps({
            "policy_status": "CONDITIONAL",
            "conditions": ["ADD_GUARANTOR"],
            "hard_stop": False,
            "policy_references": ["CREDIT-POL-4.2"]
        })

def get_llm():
    mode = os.getenv("EXECUTION_MODE", "local")
    
    if mode == "ci":
        return FakeLLM()

    if os.getenv("EXECUTION_MODE") == "azure":
        return AzureOpenAIProvider(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_SUBSCRIPTION"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        )
    return OllamaProvider()

def get_policy_search_client():
    if os.getenv("USE_AZURE_SEARCH") == "true":
        return PolicySearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY")
        )

    # fallback (optional, but keep it for safety)
    class FakePolicySearchClient:
        def search(self, query: str, top_k: int = 5):
            return [
                "CREDIT-POL-4.2: Applicants with credit score below 720 require a guarantor."
            ]

    return FakePolicySearchClient()
