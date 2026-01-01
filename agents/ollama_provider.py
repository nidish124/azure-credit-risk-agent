from config.token_budget import AGENT_TOKEN_LIMITS
from agents.llm_provider import LLMProvider
import ollama
import json
import logging
logger = logging.getLogger("credit_decision")
class OllamaProvider(LLMProvider):
    def __init__(self, agent_name: str, model: str = "llama3.2:latest"):
        self.model = model
        self.agent_name = agent_name

    def generate(self, prompt: str, max_tokens: int = None, schema: dict | None = None) -> str:
        if max_tokens is None:
            max_tokens = AGENT_TOKEN_LIMITS.get(self.agent_name, 1500)
        try:
            response_dict = ollama.generate(
                model=self.model,
                prompt = prompt,
                stream=False,
                format = "json",
                options={
                "num_predict": max_tokens,
                "temperature": 0.0,
                "seed": 42
            }
            )
            usage = {
                "prompt_tokens": response_dict.get("prompt_eval_count", 0),
                "completion_tokens": response_dict.get("eval_count", 0),
                "total_tokens": response_dict.get("prompt_eval_count", 0) + response_dict.get("eval_count", 0),
            }
            logger.info(f"LLM Token Usage (Ollama): "
                f"Prompt: {usage['prompt_tokens']}, "
                f"Completion: {usage['completion_tokens']}, "
                f"Total: {usage['total_tokens']}")
                
            logger.info(f"RAW OLLAMA RESPONSE DICT: {response_dict}")

            raw = response_dict.get("response", "")
            if not isinstance(raw, str):
                raw = json.dumps(raw)
            
            return raw

        except ollama.RequestError as e:
            print(f"Ollama API Error (Code {e.status_code}): Ensure server is running and model '{self.model}' is pulled.")
            return f"Error: Could not generate response."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return f"Error: An unexpected issue occurred."
        