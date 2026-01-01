from collections import Counter

class DecisionMetrics:
    def __init__(self):
        self.decisions = []
        self.risk_band = []

    def record(self, decision_output, risk_output):
        self.decisions.append(decision_output.recommendation)
        self.risk_band.append(risk_output.risk_band)

    def summary(self):
        return {
            "decision_distribution": dict(Counter(self.decisions)),
            "risk_band_distribution": dict(Counter(self.risk_band))
        }