import os
from dotenv import load_dotenv
from agents.ollama_provider import OllamaProvider
from agents.azure_openai_provider import AzureOpenAIProvider
from agents.search.policy_search import PolicySearchClient

load_dotenv()

def get_llm():
    if os.getenv("USE_AZURE_OPENAI") == "true":
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
