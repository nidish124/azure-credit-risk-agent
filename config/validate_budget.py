from config.token_budget import (
    MAX_TOTAL_TOKENS,
    AGENT_TOKEN_LIMITS,
    SYSTEM_TOKEN_BUFFER,
)

def validate_token_budget():
    allocated = sum(AGENT_TOKEN_LIMITS.values()) + SYSTEM_TOKEN_BUFFER

    if allocated > MAX_TOTAL_TOKENS:
        raise ValueError(
            f"Token budget exceeded: allocated={allocated}, "
            f"max={MAX_TOTAL_TOKENS}"
        )