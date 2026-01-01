from config.token_budget import AGENT_TOKEN_LIMITS
from openai import AzureOpenAI
from agents.llm_provider import LLMProvider
import logging

logger = logging.getLogger("credit_decision")

class AzureOpenAIProvider(LLMProvider):
    def __init__(
        self, endpoint: str, api_key: str, 
        deployment_name: str, api_version: str = "2024-12-01-preview",
        max_tokens:int = 1500
        ):

        self.client = AzureOpenAI(
        azure_endpoint = endpoint,
        api_key=api_key,
        api_version=api_version
        )
        self.max_tokens = max_tokens
        self.api_version = api_version
        self.deployment_name = deployment_name

    def generate(self, prompt: str, max_tokens: int,schema: dict | None = None) -> str:
        
        # if not self.max_tokens:
        #     max_tokens = AGENT_TOKEN_LIMITS.get(agent_name)
        kwargs = {
            "model": self.deployment_name,
            "messages": [
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "max_completion_tokens": self.max_tokens,
            #"temperature": 0,
        }

        if schema:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_output",
                    "schema": schema,
                },
            }
        logger.error(
            f"USING AZURE DEPLOYMENT: {self.deployment_name}, {self.api_version}"
        )
        respond = self.client.chat.completions.create(**kwargs)
        logger.info(f"RAW RESPONSE:   {respond}")
        # respond = self.client.chat.completions.create(
        #     model=self.deployment_name,
        #     messages = [
        #         {"role": "system", "content": "you must return strict JSON only."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     #temperature = 1,
        #     max_completion_tokens=max_tokens,
        #     #seed=42
        # )

        usage = respond.usage

        logger.info(f"LLM Token Usage: "
            f"Prompt: {usage.prompt_tokens}, "
            f"Completion: {usage.completion_tokens}, "
            f"Total: {usage.total_tokens}")

        content = respond.choices[0].message.content
        if not content or not content.strip():
            raise RuntimeError("Empty LLM response under JSON schema enforcement")

        return content


    
