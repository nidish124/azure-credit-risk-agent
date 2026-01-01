import time
import requests

URL = "http://localhost:8000/credit/evaluate"

PAYLOAD = {
    "application_id": "bench-1",
    "applicant_id": "user-1",
    "employment_type": "SALARIED",
    "monthly_income": 50000,
    "existing_emi": 10000,
    "credit_score": 720,
    "loan_amount": 10000,
    "loan_tenure_months": 36,
    "product_type": "PERSONAL_LOAN",
    "channel": "DIGITAL",
    "declared_assets_value": 500000
}

RUNS = 10

def run():
    latencies = []
    failures = 0

    for i in range(RUNS):
        start = time.time()
        r = requests.post(URL, json=PAYLOAD)
        elapsed = time.time() - start
        latencies.append(elapsed)

        if r.status_code != 200:
            failures += 1

    print("avg_latency_sec:", sum(latencies) / len(latencies))
    print("max_latency_sec:", max(latencies))
    print("failures:", failures)

if __name__ == "__main__":
    run()
