from abc import ABC, abstractmethod
from typing import List, Optional

class LLMProvider(ABC):
    @abstractmethod
    def get_response(
        self, 
        prompt: str, 
        system: str = "", 
        message: str = "--- 🧠 Analyzing with LLM ",
        images: Optional[List[str]] = None
    ) -> str:
        """
        Get response from LLM
        
        Args:
            prompt: Text prompt
            system: System prompt
            message: Progress message for terminal
            images: List of image file paths or base64 strings
        """
        pass
