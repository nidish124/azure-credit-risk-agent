from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int) -> str:
        print("Noting is passed in generate")
        pass