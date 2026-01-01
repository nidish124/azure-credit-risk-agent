from config.token_budget import AGENT_TOKEN_LIMITS
from agents.base_llm_agent import BaseLLMAgent
import json
from agents.llm_provider import LLMProvider
from contracts.agents.explanation_agent_contract import ExplanationAgentOutput

max_token = AGENT_TOKEN_LIMITS["explanation_agent"]

class ExplainabilityAgent(BaseLLMAgent):
    def __init__(self, llm: LLMProvider, prompt_template: str):
        super().__init__(
            llm=llm,
            prompt_template=prompt_template,
            output_model=ExplanationAgentOutput,
            agent_name="explanation_agent",
            primary_max_tokens=int(AGENT_TOKEN_LIMITS["explanation_agent"]),
            retry_max_tokens=int((AGENT_TOKEN_LIMITS["explanation_agent"])*2),
        )
    def run(self, input_data):
        try:
            return super().run(input_data.model_dump_json())
        except Exception:
            return ExplanationAgentOutput(
                summary = "Explanation unavailable",
                key_points = []
            )

# class ExplainabilityAgent:
#     def __init__(self, llm: LLMProvider, prompt_template: str):
#         self.llm = llm
#         self.prompt_template = prompt_template

#     def run(self, inp: ExplanationAgentInput) -> ExplanationAgentOutput:
#         prompt = f"""
#         {self.prompt_template}

#         Risk output:
#         {inp.risk_output.model_dump_json()}

#         Policy Output:
#         {inp.policy_output.model_dump_json()}
#         """

#         raw = self.llm.generate(prompt)

#         try:
#             parsed = json.loads(raw)
#             return ExplanationAgentOutput(**parsed)

#         except Exception as e:
#             raise RuntimeError(f"Invalid explanation output: {raw}") from e
