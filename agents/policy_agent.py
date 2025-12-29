from bokeh.themes._caliber import json
import json
from agents.llm_provider import LLMProvider
from agents.search.policy_search import PolicySearchClient
from contracts.agents.policy_agent_contract import (
    PolicyAgentInput,
    PolicyAgentOutput
)
import logging
logger = logging.getLogger("credit_decision")

class PolicyInterpretationAgent:
    def __init__(
        self,
        llm: LLMProvider,
        search_client: PolicySearchClient,
        prompt_template: str):

        self.llm = llm
        self.search_client = search_client
        self.prompt_template = prompt_template

    def run(self, inp: PolicyAgentInput) -> PolicyAgentOutput:
        query = (
            f"Loan policy for {inp.application.product_type}, "
            f"credit score {inp.application.credit_score}, "
            f"risk band {inp.risk_output.risk_band}"
        )

        policy_docs = self.search_client.search(query)
        
        logger.info(
            f"Policy search executed | query='{query}' | docs_retrieved={len(policy_docs)}"
        )

        logger.info(
            f"Policy documents retrieved: {policy_docs}"
        )
        
        prompt = f"""
        {self.prompt_template}

        Applicant:
        {inp.application.model_dump_json()}

        Risk Output:
        {inp.risk_output.model_dump_json()}

        Policy Clauses:
        {policy_docs}
        """

        raw = self.llm.generate(prompt)

        logger.info(
            f"LLM Used: {self.llm}, output of raw: {raw}"
        )

        try:
            parsed = json.loads(raw)
            return PolicyAgentOutput(**parsed)
        except Exception as e:
            raise RuntimeError(f"Invalid Policy agent output: {raw}") from e


