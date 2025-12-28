import json
from agents.llm_provider import LLMProvider
from contracts.agents.explanation_agent_contract import (
    ExplanationAgentInput,
    ExplanationAgentOutput
)

class ExplainabilityAgent:
    def __init__(self, llm: LLMProvider, prompt_template: str):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, inp: ExplanationAgentInput) -> ExplanationAgentOutput:
        prompt = f"""
        {self.prompt_template}

        Risk output:
        {inp.risk_output.model_dump_json()}

        Policy Output:
        {inp.policy_output.model_dump_json()}
        """

        raw = self.llm.generate(prompt)

        try:
            parsed = json.loads(raw)
            return ExplanationAgentOutput(**parsed)

        except Exception as e:
            raise RuntimeError(f"Invalid explanation output: {raw}") from e
