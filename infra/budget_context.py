from config.token_budget import AGENT_TOKEN_LIMITS, MAX_TOTAL_TOKENS

def get_token_budget_snapshot():
    return {
        "max_total_tokens": MAX_TOTAL_TOKENS,
        "agent_limits": AGENT_TOKEN_LIMITS
    }
