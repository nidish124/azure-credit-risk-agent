from evaluation.decision_metrics import DecisionMetrics
from evaluation.rag_metrics import RAGMetrics
from evaluation.agent_metrics import AgentMetrics

class MetricsRegistry:
    decision = DecisionMetrics()
    rag = RAGMetrics()
    agent = AgentMetrics()

    @classmethod
    def snapshot(cls):
        return {
            "decision_metrics": cls.decision.summary(),
            "rag_metrics": cls.rag.summary(),
            "agent_metrics": cls.agent.summary()
        }