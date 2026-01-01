from infra.token_counter import estimate_tokens
from config.llm_costs import MODEL_COSTS
class TokenTracker:
    """
    Tracks estimated token usage per agent and total per request.
    """

    def __init__(self):
        self._usage = {}
        self.records = []

    def record(self, agent_name: str, text: str):
        tokens = estimate_tokens(text)
        self._usage[agent_name] = self._usage.get(agent_name, 0) + tokens

    def total_tokens(self) -> int:
        return sum(self._usage.values())

    def breakdown(self) -> dict:
        return dict(self._usage)

    def record_llm_usage(
        self,
        agent_name: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        ):
        pricing = MODEL_COSTS[model]

        cost = (
            (prompt_tokens/1000) * pricing["prompt"] 
            + (completion_tokens/1000) * pricing["completion"]
        )
        self.records.append({
            "agent": agent_name,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost": cost,
        })

    def total_cost(self) -> float:
        return sum(r["cost"] for r in self.records)

    def per_agent_cost(self):
        result = {}
        for r in self.records:
            result.setdefault(r["agent"], 0)
            result[r["agent"]] += r["cost"]
        return result       