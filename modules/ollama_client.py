"""
Ollama Client for PageIndex Testing Application
Provides integration with local Ollama instance
"""

import requests
import json
from typing import Optional, Dict, Any, AsyncIterator


class OllamaClient:
    """Client for interacting with local Ollama instance"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "granite3-dense:8b"):
        """
        Initialize Ollama client
        
        Args:
            base_url: Base URL for Ollama API
            model: Model name to use
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception:
            return []
    
    def generate(self, prompt: str, temperature: float = 0.0, stream: bool = False) -> str:
        """
        Generate completion from Ollama
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            stream: Whether to stream response
            
        Returns:
            Generated text
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                if stream:
                    # Handle streaming response
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'response' in data:
                                full_response += data['response']
                    return full_response
                else:
                    data = response.json()
                    return data.get('response', '')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
    
    async def chat_completion(
        self,
        messages: list,
        temperature: float = 0.0,
        stream: bool = False
    ) -> str:
        """
        Chat completion compatible with OpenAI format
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            stream: Whether to stream response
            
        Returns:
            Generated response
        """
        # Convert messages to single prompt
        prompt = self._messages_to_prompt(messages)
        return self.generate(prompt, temperature, stream)
    
    def _messages_to_prompt(self, messages: list) -> str:
        """Convert OpenAI-style messages to a single prompt"""
        prompt_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            if role == 'system':
                prompt_parts.append(f"System: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def chat_with_vision(
        self,
        prompt: str,
        image_paths: Optional[list] = None,
        temperature: float = 0.0
    ) -> str:
        """
        Chat with vision support (for multimodal models)
        
        Args:
            prompt: Text prompt
            image_paths: List of image file paths
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        # For vision models, we need to use the /api/generate endpoint with images
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        # Add images if provided
        if image_paths:
            import base64
            images = []
            for img_path in image_paths:
                try:
                    with open(img_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')
                        images.append(img_data)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
            
            if images:
                payload['images'] = images
        
        try:
            response = requests.post(url, json=payload, timeout=180)
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


# Async wrapper for compatibility with OpenAI-style async calls
class AsyncOllamaClient:
    """Async wrapper for OllamaClient"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "granite3-dense:8b"):
        self.client = OllamaClient(base_url, model)
    
    async def chat_completions_create(
        self,
        model: str,
        messages: list,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        """
        Create chat completion (async compatible)
        
        Returns:
            Dict with OpenAI-compatible structure
        """
        response_text = await self.client.chat_completion(messages, temperature)
        
        return {
            "choices": [
                {
                    "message": {
                        "content": response_text
                    }
                }
            ]
        }

# Made with Bob
