from infra.token_counter import estimate_tokens
from infra.prompt_guard import trim_text_to_token_budget

def limit_rag_context(
    documents: list[str],
    max_tokens: int
    ) -> list[str]:
    final_docs = []
    used_tokens = 0

    for doc in documents:
        doc_tokens = estimate_tokens(doc)
        if used_tokens + doc_tokens > max_tokens:
            remaining = max_tokens - used_tokens
            if remaining <= 0:
                break

            doc = trim_text_to_token_budget(doc, remaining)
            doc_tokens = estimate_tokens(doc)

        final_docs.append(doc)
        used_tokens += doc_tokens

    return final_docs

