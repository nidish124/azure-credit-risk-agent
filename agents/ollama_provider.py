from agents.llm_provider import LLMProvider
import ollama
import json

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model

    def generate(self, prompt: str) -> str:

        try:
            response_dict = ollama.generate(
                model=self.model,
                prompt = prompt,
                stream=False,
                format = "json"
            )

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
        