import json
from openai import AzureOpenAI
from agents.llm_provider import LLMProvider

class AzureOpenAIProvider(LLMProvider):
    def __init__(
        self, endpoint: str, api_key: str, 
        deployment_name: str, api_version: str = "2024-12-01-preview"
        ):

        self.client = AzureOpenAI(
        azure_endpoint = endpoint,
        api_key=api_key,
        api_version=api_version
        )

        self.deployment_name = deployment_name

    def generate(self, prompt: str) -> str:
        respond = self.client.chat.completions.create(
            model=self.deployment_name,
            messages = [
                {"role": "system", "content": "you mush return strict JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature = 1,
        )

        content = respond.choices[0].message.content
        return content
