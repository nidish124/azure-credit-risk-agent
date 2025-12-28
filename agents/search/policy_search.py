from typing import List
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os 
from dotenv import load_dotenv

load_dotenv()


class PolicySearchClient:
    def __init__(self, endpoint: str, index_name: str, api_key: str):
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )

    def search(self, query: str, top_k: int = 5) -> List[str]:
        results = self.client.search(query, top=top_k)

        documents = []
        for result in results:
            documents.append(result["content"])

        return documents

def get_policy_search_client():
    return PolicySearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX"),
        api_key=os.getenv("AZURE_SEARCH_API_KEY")
        )
