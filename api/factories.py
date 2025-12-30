import os
from dotenv import load_dotenv
from agents.ollama_provider import OllamaProvider
from agents.azure_openai_provider import AzureOpenAIProvider
from agents.search.policy_search import PolicySearchClient
import json
import logging
logger = logging.getLogger("credit_decision")
load_dotenv(override=True)

class FakeLLM:
    def generate(self, prompt: str) -> str:
        # Risk Agent
        if "risk_band" in prompt and "risk_factors" in prompt and "credit risk analysis system" in prompt:
            return json.dumps({
                "risk_band": "MEDIUM",
                "risk_factors": [
                    {"factor": "Credit Score", "impact": "HIGH"}
                ],
                "data_quality_issues": []
            })
        
        # Policy Agent
        elif "policy_status" in prompt and "hard_stop" in prompt and "banking credit policy interpretation system" in prompt:
            return json.dumps({
                "policy_status": "CONDITIONAL",
                "conditions": ["ADD_GUARANTOR"],
                "hard_stop": False,
                "policy_references": ["CREDIT-POL-4.2"]
            })

        # Explanation Agent
        elif "risk_references" in prompt and "policy_references" in prompt and "audit explanation system" in prompt:
            return json.dumps({
                "summary": "Application requires conditional approval due to a policy exception and medium risk profile.",
                "key_reasons": ["Credit score is below 720", "Policy requires an added guarantor"],
                "risk_references": ["Credit Score", "Loan to Income Ratio"],
                "policy_references": ["CREDIT-POL-4.2"]
            })
        else:
            return json.dumps({"error": f"Unknown prompt received: {prompt[:50]}..."})

def get_llm():
    mode = os.getenv("EXECUTION_MODE", "local")
    logger.info(
            f"LLM retrieved from execution mode is : {mode}"
        )
    if mode == "ci":
        return FakeLLM()

    if mode == "azure":
        return AzureOpenAIProvider(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_SUBSCRIPTION"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        )
    return OllamaProvider()

def get_policy_search_client():
    mode = os.getenv("EXECUTION_MODE", "local")
    if mode == "azure":
        return PolicySearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY")
        )

    # fallback (optional, but keep it for safety)
    class FakePolicySearchClient:
        def search(self, query: str, top_k: int = 5):
            return [
                "CREDIT-POL-4.2.1: Applicants with credit score below 720 require a guarantor. "
            ]

    return FakePolicySearchClient()
