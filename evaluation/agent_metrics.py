class AgentMetrics:
    def __init__(self):
        self.stats = {}

    def _get(self, agent):
        return self.stats.setdefault(
            agent,
            {"calls": 0, "retries": 0, "failures": 0}
        )

    def record_success(self, agent):
        self._get(agent)["calls"] += 1

    def record_retry(self, agent):
        self._get(agent)["retries"] += 1

    def record_failure(self, agent):
        self._get(agent)["failures"] += 1

    def summary(self):
        return {
            "retry_rate": self.stats.get("retries",0) / max(self.stats.get("calls",0), 1),
            "failure_rate": self.stats.get("failures",0) / max(self.stats.get("calls",0), 1),
        }
