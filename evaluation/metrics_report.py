from evaluation.agent_metrics import AgentMetrics
from evaluation.rag_metrics import RAGMetrics
from evaluation.decision_metrics import DecisionMetrics

class MetricsReport:
    def __init__(self):
        self.decision = DecisionMetrics()
        self.rag = RAGMetrics()
        self.agent = AgentMetrics()

    def snapshot(self):
        return {
            "decision_metrics": self.decision.summary(),
            "rag_metrics": self.rag.summary(),
            "agent_metrics": self.agent.summary(),
        }
