from prometheus_client import Counter, Histogram, Gauge

# Requests
REQUEST_COUNT = Counter(
    "credit_requests_total",
    "Total credit evaluation requests",
)

REQUEST_FAILURES = Counter(
    "credit_requests_failed_total",
    "Total failed credit evaluation requests",
)

# Latency
REQUEST_LATENCY = Histogram(
    "credit_request_latency_seconds",
    "Credit evaluation latency",
    buckets=(0.5, 1, 2, 3, 5, 7, 10, 15),
)

# Tokens
TOKENS_USED = Counter(
    "llm_tokens_total",
    "Total LLM tokens used",
    ["agent", "model"],
)

# Cost
REQUEST_COST = Histogram(
    "credit_request_cost_usd",
    "Cost per credit evaluation request (USD)",
    buckets=(0.0005, 0.001, 0.002, 0.005, 0.01, 0.02),
)

# RAG
RAG_HITS = Counter(
    "rag_hits_total",
    "Total RAG successful retrievals",
)

RAG_MISSES = Counter(
    "rag_misses_total",
    "Total RAG misses",
)
