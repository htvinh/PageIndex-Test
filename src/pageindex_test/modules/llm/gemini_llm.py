from fast_cli.llm.base import LLMProvider
from google import genai
from google.genai import types
import sys

class GeminiLLM(LLMProvider):
    def __init__(self, api_key: str, model_name: str, temperature: float):
        if not api_key:
            raise ValueError("API key required for GeminiLLM")
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature

    def get_response(self, prompt: str, system: str = "", message: str = "--- 🧠 Analyzing with LLM (Gemini)... ") -> str:
        sys.stdout.write(message)
        sys.stdout.flush()
        full_prompt = (system + "\n" if system else "") + prompt
        resp = self.client.models.generate_content(
            model=self.model_name,
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                    temperature=self.temperature,
            )
        )
        sys.stdout.write(" [Done]\n")
        sys.stdout.flush()
        return resp.text.strip()
