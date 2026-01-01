from infra.rag_guard import limit_rag_context
from infra.token_counter import estimate_tokens

def test_rag_context_respects_token_limit():
    docs = [
        "A" * 4000,
        "B" * 4000,
        "C" * 4000
    ]
    limited = limit_rag_context(docs, max_tokens=1000)

    total_tokens = sum(estimate_tokens(d) for d in limited)
    assert total_tokens <= 1000
    assert len(max(limited, key=len)) > 1

def test_rag_context_handles_empty_input():
    assert limit_rag_context([], 500) == []