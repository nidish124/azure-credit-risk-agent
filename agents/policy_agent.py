from agents.base_llm_agent import BaseLLMAgent
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
        policy_docs = self.search_client.search(query)

        policies = self.prepare_policy_context(policy_docs)

        # policies = self.search_client.search(query)

        input_payload = {
            "application": input_data.application.model_dump(),
            "risk_output": input_data.risk_output.model_dump(),
            "policies": policies,
        }

        return super().run(json.dumps(input_payload))

# class PolicyInterpretationAgent:
#     def __init__(
#         self,
#         llm: LLMProvider,
#         search_client: PolicySearchClient,
#         prompt_template: str):

#         self.llm = llm
#         self.search_client = search_client
#         self.prompt_template = prompt_template

#     def prepare_policy_context(self, retrieved_policies: list[str]) -> list[str]:
#         limited = limit_rag_context(
#             retrieved_policies,
#             AGENT_TOKEN_LIMITS["policy_agent"]
#             )
#         logger.info(
#             "rag_context_limited", extra={"orignial_docs": len(retrieved_policies), "final_docs": len(limited)}
#             )
#         return limited

#     def run(self, inp: PolicyAgentInput) -> PolicyAgentOutput:
#         query = (
#             f"Loan policy for {inp.application.product_type}, "
#             f"credit score {inp.application.credit_score}, "
#             f"risk band {inp.risk_output.risk_band}"
#         )

#         policy_docs = self.search_client.search(query)

#         policies = self.prepare_policy_context(policy_docs)

#         logger.info(
#             f"Policy search executed | query='{query}' | docs_retrieved={len(policies)}"
#         )

#         logger.info(
#             f"Policy documents retrieved: {policies}"
#         )
        
#         prompt = f"""
#         {self.prompt_template}

#         Applicant:
#         {inp.application.model_dump_json()}

#         Risk Output:
#         {inp.risk_output.model_dump_json()}

#         Policy Clauses:
#         {policies}
#         """

#         raw = self.llm.generate(prompt)

#         logger.info(
#             f"LLM Used: {self.llm}, output of raw: {raw}"
#         )

#         try:
#             parsed = json.loads(raw)
#             return PolicyAgentOutput(**parsed)
#         except Exception as e:
#             raise RuntimeError(f"Invalid Policy agent output: {raw}") from e

