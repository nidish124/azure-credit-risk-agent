class RAGMetrics:
    def __init__(self):
        self.calls = 0
        self.fallbacks = 0
        self.docs_retrieved = []

    def record(self, retrieved_docs, fallback_used: bool):
        self.calls += 1
        self.docs_retrieved.append(len(retrieved_docs))
        if fallback_used:
            self.fallbacks += 1

    def summary(self):
        return {
            "avg_docs_retrieved": sum(self.docs_retrieved) / max(len(self.docs_retrieved),1),
            "fallback_rate": self.fallbacks / max(self.calls, 1)
        }