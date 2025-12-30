from api.factories import get_policy_search_client

def retrieve_policies(query: str) -> list[str]:
    return get_policy_search_client().search(query)