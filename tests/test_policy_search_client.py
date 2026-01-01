from unittest.mock import MagicMock
from agents.tools.policy_search import PolicySearchClient


def test_embed_returns_vector():
    client = PolicySearchClient(
        search_endpoint="https://test.search.windows.net",
        search_index_name="policies",
        search_api_key="fake",
        embed_endpoint="https://test.openai.azure.com",
        embed_model_version="2024-02-01",
        embed_api_key="fake",
        embed_model_name="text-embedding-3-large"
    )

    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    client.embed_client.embeddings.create = MagicMock(return_value=mock_response)

    vector = client.embed("test query")

    assert isinstance(vector, list)
    assert len(vector) == 3

from unittest.mock import MagicMock
from agents.tools.policy_search import PolicySearchClient

def test_hybrid_search_returns_results():
    client = PolicySearchClient(
        search_endpoint="https://test.search.windows.net",
        search_index_name="policies",
        search_api_key="fake",
        embed_endpoint="https://test.openai.azure.com",
        embed_model_version="2024-02-01",
        embed_api_key="fake",
        embed_model_name="text-embedding-3-large"
    )

    # Mock embedding
    client.embed = MagicMock(return_value=[0.1, 0.2, 0.3])

    # Mock search results
    mock_result = {"content": "Policy clause text"}
    client.search_client.search = MagicMock(return_value=[mock_result])

    results = client.search("DTI threshold")

    assert len(results) == 1
    assert "Policy clause" in results[0]

    # Ensure hybrid search was called
    client.search_client.search.assert_called_once()

def test_keyword_fallback_when_vector_returns_empty():
    client = PolicySearchClient(
        search_endpoint="https://test.search.windows.net",
        search_index_name="policies",
        search_api_key="fake",
        embed_endpoint="https://test.openai.azure.com",
        embed_model_version="2024-02-01",
        embed_api_key="fake",
        embed_model_name="text-embedding-3-large"
    )

    client.embed = MagicMock(return_value=[0.1, 0.2, 0.3])

    # First call → empty (vector search)
    # Second call → keyword fallback
    client.search_client.search = MagicMock(
        side_effect=[
            [],  # hybrid search returns nothing
            [{"content": "Fallback policy text"}]  # keyword fallback
        ]
    )

    results = client.search("Collateral requirements")

    assert len(results) == 1
    assert "Fallback policy" in results[0]

def test_search_ignores_documents_without_content():
    client = PolicySearchClient(
        search_endpoint="https://test.search.windows.net",
        search_index_name="policies",
        search_api_key="fake",
        embed_endpoint="https://test.openai.azure.com",
        embed_model_version="2024-02-01",
        embed_api_key="fake",
        embed_model_name="text-embedding-3-large"
    )

    client.embed = MagicMock(return_value=[0.1, 0.2, 0.3])

    client.search_client.search = MagicMock(
        return_value=[{"content": None}, {"content": "Valid clause"}]
    )

    results = client.search("Loan policy")

    assert results == ["Valid clause"]
