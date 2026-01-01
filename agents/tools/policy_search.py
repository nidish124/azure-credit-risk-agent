from openai.lib.azure import AzureOpenAI
from typing import List
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os 
from dotenv import load_dotenv
import logging
logger = logging.getLogger("credit_decision")
load_dotenv(override=True)

class PolicySearchClient:
    def __init__(self, search_endpoint: str, search_index_name: str, search_api_key: str, 
                    embed_endpoint: str, embed_model_version: str, embed_api_key: str, embed_model_name: str):
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=search_index_name,
            credential=AzureKeyCredential(search_api_key)
        )
        self.embed_client = AzureOpenAI(
            azure_endpoint=embed_endpoint,
            api_key=embed_api_key,
            api_version=embed_model_version
        )
        self.embed_model_name = embed_model_name

    def embed(self, text: str):
        response = self.embed_client.embeddings.create(
            model=self.embed_model_name,
            input = text
        )
        return response.data[0].embedding

    def search(self, query: str, top_k: int = 5) -> List[str]:
        """Hybrid retrieval:
            - Keyword search
            - vector search
        """
        query_embedding = self.embed(query)
        results = self.search_client.search(
            search_text=query,
            select=["content"],
            vector_queries=[
                {
                    "vector": query_embedding,
                    "fields": "contentVector",
                    "k": top_k,
                    "kind": "vector"
                }
            ],
            top = top_k
        )
        
        results_list = list(results)

        if not results_list:
            logger.info(
            f"Policy search fallback to keywork-only search | query='{query}'"
            )
            results = self.search_client.search(search_text=query, top=top_k)
            results_list = list(results)

        return [r.get("content") for r in results_list if r.get("content")]
