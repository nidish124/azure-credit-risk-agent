from evaluation.registry import MetricsRegistry
from evaluation.rag_metrics import RAGMetrics
from agents.base_llm_agent import BaseLLMAgent
from monitoring.prometheus_metrics import RAG_HITS, RAG_MISSES
import json
from agents.llm_provider import LLMProvider
from agents.tools.policy_search import PolicySearchClient
from contracts.agents.policy_agent_contract import (
    PolicyAgentInput,
    PolicyAgentOutput
)
from config.token_budget import AGENT_TOKEN_LIMITS
from infra.rag_guard import limit_rag_context
import logging
logger = logging.getLogger("credit_decision")

class PolicyInterpretationAgent(BaseLLMAgent):
    def __init__(self, llm: LLMProvider, search_client, prompt_template: str):
        self.search_client : PolicySearchClient = search_client
        super().__init__(
            llm =llm,
            prompt_template=prompt_template,
            output_model=PolicyAgentOutput,
            agent_name="policy_agent",
            primary_max_tokens=int(AGENT_TOKEN_LIMITS["policy_agent"]),
            retry_max_tokens=int((AGENT_TOKEN_LIMITS["policy_agent"])*2),
        )
    
    def prepare_policy_context(self, retrieved_policies: list[str]) -> list[str]:
        limited = limit_rag_context(
            retrieved_policies,
            AGENT_TOKEN_LIMITS["policy_agent"]
            )
        logger.info(
            "rag_context_limited", extra={"orignial_docs": len(retrieved_policies), "final_docs": len(limited)}
            )
        return limited

    def run(self, input_data:PolicyAgentInput):
        query = (
            f"Loan policy for {input_data.application.product_type}, "
            f"credit score {input_data.application.credit_score}, "
            f"risk band {input_data.risk_output.risk_band}"
        )

        fallback_used = False

        policy_docs = self.search_client.search(query)

        if policy_docs:
            RAG_HITS.inc()
        else:
            RAG_MISSES.inc()

        if not policy_docs:
            fallback_used = True
            policy_docs = self.search_client.keyword_search(query)
            
        MetricsRegistry.rag.record(
            retrieved_docs=policy_docs,
            fallback_used= fallback_used
        )

        policies = self.prepare_policy_context(policy_docs)

        # policies = self.search_client.search(query)

        input_payload = {
            "application": input_data.application.model_dump(),
            "risk_output": input_data.risk_output.model_dump(),
            "policies": policies,
        }

        return super().run(json.dumps(input_payload))
