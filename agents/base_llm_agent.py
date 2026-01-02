from evaluation.registry import MetricsRegistry
from evaluation.agent_metrics import AgentMetrics
from h11._abnf import method
import logging
from langchain_core.output_parsers import PydanticOutputParser

logger = logging.getLogger("credit_decision")

class BaseLLMAgent:
    def __init__(
        self,
        llm,
        prompt_template: str,
        output_model,
        agent_name: str,
        primary_max_tokens: int,
        retry_max_tokens: int,
    ):
        self.llm = llm
        self.prompt_template = prompt_template
        self.parser = PydanticOutputParser(pydantic_object=output_model)
        self.agent_name = agent_name
        self.primary_max_tokens = primary_max_tokens
        self.retry_max_tokens = retry_max_tokens

    def _build_prompt(self, input_json: str) -> str:
        return (
            self.prompt_template
            + "\n\nINPUT:\n"
            + input_json
            + "\n\nOUTPUT FORMAT:\n"
            + self.parser.get_format_instructions()
        )

    def run(self, input_json: str):
        prompt = self._build_prompt(input_json)
        schema = self.parser.pydantic_object.model_json_schema()

        try:
            raw = self.llm.generate(
                prompt, 
                max_tokens=self.primary_max_tokens,
                schema=schema,
            )
            MetricsRegistry.agent.record_success(self.agent_name)
            return self.parser.parse(raw)

        except Exception as e:
            logger.warning(
                "llm_output_parse_failed_retrying",
                extra={
                    "agent": self.agent_name,
                    "primary_max_tokens": self.primary_max_tokens,
                },
            )

            try:
                raw = self.llm.generate(
                    prompt,
                    max_tokens=self.retry_max_tokens,
                    schema=schema,
                )
                MetricsRegistry.agent.record_retry(self.agent_name)
                return self.parser.parse(raw)

            except Exception as e:
                if self.agent_name == "explanation_agent":
                    logger.error("explanation_fallback_used")

                    MetricsRegistry.agent.record_failure(self.agent_name)

                    return self.parser.pydantic_object(
                        summary="Decision explanation unavailable due to token limits.",
                        key_reasons=[]
                    )
                raise