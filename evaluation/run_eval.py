from contracts.graph_state import CreditDecisionGraphState
import json
import time
from graph.builder import build_credit_decision_graph
#from evaluation.cost import costTracker

DATASET_PATH = "evaluation/datasets/credit_eval.jsonl"
OUTPUT_MD = "evaluation/eval_report.md"
OUTPUT_JSON = "evaluation/eval_report.json"
THRESHOLD_JSON = "evaluation/thresholds.json"

def run():
    decision_correct = 0
    rag_hits = 0
    latncies = []
    costs = []

    with open(DATASET_PATH) as f:
        cases = [json.loads(line) for line in f]

    for case in cases:
        start = time.perf_counter()

        final_state = build_credit_decision_graph().invoke(
            CreditDecisionGraphState(application=case["input"])
        )
        
        latency = time.perf_counter() - start
        latncies.append(latency)
        
        print(f"latency: {latency}, {final_state['decision_output'].recommendation}")

        if final_state["decision_output"].recommendation == case["expected"]["decision"]:
            decision_correct += 1

        print(f"latency: {latency} | {final_state['decision_output'].recommendation} | recommened: {case["expected"]["decision"]} ")

        if final_state["policy_output"].policy_references:
            rag_hits += 1

        costs.append(final_state["token_tracker"].total_cost())

    report = {
        "total_cases": len(cases),
        "decision_accuracy": decision_correct / len(cases),
        "rag_hit_rate": rag_hits / len(cases),
        "p50_latency_ms": sorted(latncies)[len(latncies)//2] * 1000,
        "p95_latency_ms": sorted(latncies)[int(len(latncies)*0.95)] * 1000,
        "avg_cost_per_request": sum(costs) / int(len(costs)),
    }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(report, f, indent=2)

    generate_markdown(report)

    print(json.dumps(report, indent=2))

    apply_quality_gates(report)

def generate_markdown(report: dict):
    md = f"""
    
## Automated Evaluation Results

| Metric | Value |
|------|------|
| Total Cases | {report['total_cases']} |
| Decision Accuracy | {report['decision_accuracy']} |
| RAG Hit Rate | {report['rag_hit_rate']} |
| p50 Latency | {report['p50_latency_ms']} ms |
| p95 Latency | {report['p95_latency_ms']} ms |
| Avg Cost / Request | ${report['avg_cost_per_request']} |

"""
    with open(OUTPUT_MD, "w") as f:
        f.write(md.strip())

def apply_quality_gates(report: dict):
    with open(THRESHOLD_JSON) as f:
        thresholds = json.load(f)

    failures = []

    if report["decision_accuracy"] < thresholds["decision_accuracy_min"]:
        failures.append("Decision accurary below threshold")

    if report["rag_hit_rate"] < thresholds["rag_hit_rate_min"]:
        failures.append("rag hit rate below threshold")

    if report["p95_latency_ms"] > thresholds["P95_latency_ms_max"]:
        failures.append("p95 latency above threshold")

    if report["avg_cost_per_request"] > thresholds["avg_cost_per_request_max"]:
        failures.append("Average cost per request above threshold")

    if failures:
        print("\n Quality Gates FAILD: ")
        for f in failures:
            print(f" - {f}")
        raise SystemExit(1)

    print("\n All quality gates passed.")

if __name__ == "__main__":
    run()