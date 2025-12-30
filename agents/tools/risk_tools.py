from typing import Dict

def normalize_credit_score(score: int) -> Dict[str, str]:
    if score >= 750:
        return {"band": "EXCELLENT"}
    if score >= 700:
        return {"band": "GOOD"}
    return {"band": "RISKY"}
