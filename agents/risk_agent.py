from config.token_budget import AGENT_TOKEN_LIMITS
from agents.llm_provider import LLMProvider
from agents.base_llm_agent import BaseLLMAgent
from contracts.agents.risk_agent_contract import RiskAgentOutput


class RiskScoringAgent(BaseLLMAgent):
    def __init__(self, llm: LLMProvider, prompt_template: str):
        super().__init__(
            llm=llm,
            prompt_template=prompt_template,
            output_model=RiskAgentOutput,
            agent_name="risk_agent",
            primary_max_tokens=int(AGENT_TOKEN_LIMITS["risk_agent"]),
            retry_max_tokens=int((AGENT_TOKEN_LIMITS["risk_agent"])*2),
        )

    def run(self, input_data):
        return super().run(input_data.model_dump_json())