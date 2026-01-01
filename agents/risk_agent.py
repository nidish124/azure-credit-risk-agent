from agents.llm_provider import LLMProvider
from agents.base_llm_agent import BaseLLMAgent
from contracts.agents.risk_agent_contract import RiskAgentOutput


# class RiskScoringAgent:
#     def __init__(self, llm: LLMProvider, prompt_template: str):
#         self.llm = llm
#         self.prompt_template = prompt_template
#     def run(self, inp: RiskAgentInput) -> RiskAgentOutput:
#         prompt = f"""
# {self.prompt_template}
# Applicant Data:
# {inp.application.model_dump_json()}
# """
#         raw_output = self.llm.generate(prompt)
#         try:
#             parsed = json.loads(raw_output)
#             return RiskAgentOutput(**parsed)
#         except Exception as e:
#             print("RAW OUTPUT", raw_output)
#             raise RuntimeError(f"Invalid LLM output: {raw_output}") from e

class RiskScoringAgent(BaseLLMAgent):
    def __init__(self, llm: LLMProvider, prompt_template: str):
        super().__init__(
            llm=llm,
            prompt_template=prompt_template,
            output_model=RiskAgentOutput,
            agent_name="risk_agent",
            primary_max_tokens=600,
            retry_max_tokens=1200,
        )

    def run(self, input_data):
        return super().run(input_data.model_dump_json())