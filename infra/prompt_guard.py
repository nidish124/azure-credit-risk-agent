from infra.token_counter import estimate_tokens

def trim_text_to_token_budget(text: str, max_tokens: int) -> str:
    if not text:
        return text

    while estimate_tokens(text) > max_tokens:
        text = text[: int(len(text) * 0.8)]
        
    return text