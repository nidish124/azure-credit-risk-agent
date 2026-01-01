def estimate_tokens(text: str) -> int:
    """
    Conservative token estimate.
    ~4 characters per token (safe upper bound).
    """
    if not text:
        return 0
    return max(1, len(text) // 4)