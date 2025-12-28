import json
from agents.llm_provider import LLMProvider
from contracts.agents.risk_agent_contract import RiskAgentInput, RiskAgentOutput
#from contracts.risk_output import RiskEvaluationOutput


class RiskScoringAgent:
    def __init__(self, llm: LLMProvider, prompt_template: str):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, inp: RiskAgentInput) -> RiskAgentOutput:
        prompt = f"""
{self.prompt_template}

Applicant Data:
{inp.application.model_dump_json()}
"""
        raw_output = self.llm.generate(prompt)

        try:
            parsed = json.loads(raw_output)
            return RiskAgentOutput(**parsed)
        except Exception as e:
            raise RuntimeError(f"Invalid LLM output: {raw_output}") from e
