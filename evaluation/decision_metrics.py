from collections import Counter

class DecisionMetrics:
    def __init__(self):
        self.decisions = []
        self.risk_band = []
        self.policy_status = []
        self.hard_stop = []

    def record(self, decision_output, risk_output, policy_output):
        self.decisions.append(decision_output.recommendation)
        self.risk_band.append(risk_output.risk_band)
        self.policy_status.append(policy_output.policy_status)
        self.hard_stop.append(policy_output.hard_stop)

    def summary(self):
        return {
            "decision_distribution": dict(Counter(self.decisions)),
            "risk_band_distribution": dict(Counter(self.risk_band)),
            "policy_status_distribution": dict(Counter(self.policy_status)),
            "hard_stop_distribution": dict(Counter(self.hard_stop))
        }