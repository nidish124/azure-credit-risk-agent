from config.token_budget import AGENT_TOKEN_LIMITS
import os
from dotenv import load_dotenv
from agents.ollama_provider import OllamaProvider
from agents.azure_openai_provider import AzureOpenAIProvider
from agents.tools.policy_search import PolicySearchClient
import json
import logging
logger = logging.getLogger("credit_decision")
load_dotenv(override=True)

class FakeLLM:
    def generate(self, prompt: str, max_tokens: int = None ,schema: dict | None = None) -> str:
        # Risk Agent
        if "credit risk analysis system" in prompt and "risk_band" in prompt:
            return json.dumps({
                "risk_band": "MEDIUM",
                "risk_factors": [
                    {"factor": "Credit Score", "impact": "HIGH"}
                ],
                "data_quality_issues": []
            })
        
        # Policy Agent
        elif "policy interpretation engine" in prompt and "policy_status" in prompt:
            return json.dumps({
                "policy_status": "CONDITIONAL",
                "conditions": ["ADD_GUARANTOR"],
                "hard_stop": False,
                "policy_references": ["Applicants with credit score below 720 require a guarantor.",
                "The maximum loan amount is 50,000 USD."]
            })

        # Explanation Agent
        elif "summary" in prompt and "explanation for a loan decision" in prompt:
            return json.dumps({
                "summary": "Application requires conditional approval due to a policy exception and medium risk profile.",
                "key_reasons": ["Credit score is below 720", "Policy requires an added guarantor"]
            })
        else:
            return json.dumps({"error": f"Unknown prompt received: {prompt[:50]}..."})

def get_llm(agent_name: str | None = None):
    mode = os.getenv("EXECUTION_MODE", "local")
    max_tokens = None

    if agent_name:
        max_tokens = AGENT_TOKEN_LIMITS.get(agent_name)
    if mode == "ci":
        return FakeLLM()

    if mode == "azure":
        return AzureOpenAIProvider(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_SUBSCRIPTION"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            max_tokens=max_tokens
        )
    return OllamaProvider(agent_name=agent_name)

def get_policy_search_client():
    mode = os.getenv("EXECUTION_MODE", "local")
    if mode == "azure":
        return PolicySearchClient(
            search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            search_index_name=os.getenv("AZURE_SEARCH_INDEX"),
            search_api_key=os.getenv("AZURE_SEARCH_API_KEY"),
            embed_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            embed_model_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            embed_api_key=os.getenv("AZURE_OPENAI_SUBSCRIPTION"),
            embed_model_name=os.getenv("AZURE_EMBED_MODEL_NAME", "text-embedding-3-small")
        )

    # fallback (optional, but keep it for safety)
    class FakePolicySearchClient:
        def search(self, query: str, top_k: int = 5):
            return [
                "CREDIT-POL-4.2.1: Applicants with credit score below 720 require a guarantor. "
            ]

    return FakePolicySearchClient()
