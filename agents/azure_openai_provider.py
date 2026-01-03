from config.token_budget import AGENT_TOKEN_LIMITS
from monitoring.prometheus_metrics import TOKENS_USED
from openai import AzureOpenAI
from agents.llm_provider import LLMProvider
import logging
from infra.token_tracker import TokenTracker
logger = logging.getLogger("credit_decision")

class AzureOpenAIProvider(LLMProvider):
    def __init__(
        self, endpoint: str, api_key: str, 
        deployment_name: str, agent_name: str, api_version: str = "2024-12-01-preview",token_tracker: TokenTracker = None
        ):

        self.client = AzureOpenAI(
        azure_endpoint = endpoint,
        api_key=api_key,
        api_version=api_version
        )
        self.agent_name = agent_name
        self.api_version = api_version
        self.deployment_name = deployment_name
        self.token_tracker = token_tracker

    def generate(self, prompt: str, max_tokens: int,schema: dict | None = None) -> str:
        
        if not max_tokens:
            max_tokens = AGENT_TOKEN_LIMITS.get(self.agent_name)

        kwargs = {
            "model": self.deployment_name,
            "messages": [
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "max_completion_tokens": max_tokens,
        }

        if schema:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_output",
                    "schema": schema,
                },
            }
        
        respond = self.client.chat.completions.create(**kwargs)

        usage = respond.usage

        TOKENS_USED.labels(
            agent=self.agent_name,
            model=self.deployment_name
        ).inc(usage.total_tokens)

        self.token_tracker.record_llm_usage(
            agent_name=self.agent_name,
            model=self.deployment_name,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            )

        logger.info(f"LLM Token Usage for {self.agent_name}: "
            f"Prompt: {usage.prompt_tokens}, "
            f"Completion: {usage.completion_tokens}, "
            f"Total: {usage.total_tokens}")

        content = respond.choices[0].message.content
        if not content or not content.strip():
            raise RuntimeError("Empty LLM response under JSON schema enforcement")

        return content


    
