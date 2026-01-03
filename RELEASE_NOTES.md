# Release Notes

## v1.0.0 — Production Release
Date: 2026-01-01

### Highlights
- End-to-end agentic credit risk decisioning system
- Hybrid RAG (Azure AI Search + Vector embeddings)
- Token-budget enforced LLM execution
- Azure-native deployment with observability

### New Features
- Risk Scoring Agent with structured JSON enforcement
- Policy Interpretation Agent with hybrid retrieval
- Decision Synthesis with human-in-the-loop support
- Cost-per-request tracking

### Performance
- p50 latency: ~6.8s
- p95 latency: ~7.6s
- Avg token cost: ~$0.0019/request
- RAG hit rate: 100%
- Decision accuracy: 80%

### Infrastructure
- Azure Container Apps
- Azure OpenAI
- Azure AI Search (Hybrid)
- Prometheus + Grafana
- Application Insights

### Breaking Changes
- None

---
