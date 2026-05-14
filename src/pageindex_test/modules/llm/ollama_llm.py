from pageindex_test.modules.llm.base import LLMProvider
import requests
import logging
import sys
import json
import base64
import os
from typing import List, Optional

class OllamaLLM(LLMProvider):
    def __init__(self, host="127.0.0.1", port=11434, model="gemma3:12b", temperature=0.7, num_ctx=16000):
        self.host = host
        self.port = port
        self.model = model
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.logger = logging.getLogger(__name__)

    def get_response(
        self, 
        prompt: str, 
        system: str = "", 
        message: str = "--- 🧠 Analyzing with LLM ",
        images: Optional[List[str]] = None
    ) -> str:
        url = f"http://{self.host}:{self.port}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "options": {
                "temperature": self.temperature,
                "num_ctx": self.num_ctx
            },
            "stream": True
        }
        
        # Add images if provided
        if images:
            b64_images = []
            for img in images:
                if os.path.exists(img):
                    with open(img, "rb") as f:
                        b64_images.append(base64.b64encode(f.read()).decode('utf-8'))
                else:
                    # Assume it's already base64
                    b64_images.append(img)
            payload["images"] = b64_images

        import os # Ensure os is available for path check if needed, but imported at top preferred
        
        sys.stdout.write(message)
        sys.stdout.flush()

        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        output = ""
        chunk_count = 0
        for line in response.iter_lines():
            if not line: continue
            try:
                data = json.loads(line)
                if "response" in data:
                    output += data["response"]
                    chunk_count += 1
                    if chunk_count % 5 == 0:  # Show progress every 5 chunks
                        sys.stdout.write(".")
                        sys.stdout.flush()
                if data.get("done"): break
            except json.JSONDecodeError:
                continue
        
        sys.stdout.write(" [Done]\n")
        sys.stdout.flush()
        return output.strip()
