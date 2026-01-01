from infra.token_counter import estimate_tokens

class TokenTracker:
    """
    Tracks estimated token usage per agent and total per request.
    """

    def __init__(self):
        self._usage = {}

    def record(self, agent_name: str, text: str):
        tokens = estimate_tokens(text)
        self._usage[agent_name] = self._usage.get(agent_name, 0) + tokens

    def total_tokens(self) -> int:
        return sum(self._usage.values())

    def breakdown(self) -> dict:
        return dict(self._usage)