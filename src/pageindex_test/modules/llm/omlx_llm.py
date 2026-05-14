from pageindex_test.modules.llm.base import LLMProvider
from openai import OpenAI
import logging
import sys
import os
import base64
from typing import List, Optional

logger = logging.getLogger("omlx")

class OmlxLLM(LLMProvider):
    """
    Wrapper for omlx LLM engine, which is OpenAI-compatible.
    """
    def __init__(
        self, 
        api_key: str = "omlx", 
        model: str = "gemma-4-E4B-it-MLX-8bit",
        base_url: str = "http://localhost:8000/v1",
        temperature: float = 0.7
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.temperature = temperature

    def get_response(
        self, 
        prompt: str, 
        system: str = "You are a helpful assistant.",
        message: str = "--- 🧠 Analyzing with LLM (OMLX)... ",
        images: Optional[List[str]] = None
    ) -> str:
        """
        Sends `prompt` to the omlx chat completion API and returns the assistant's reply.
        Supports vision if images are provided.
        """
        sys.stdout.write(message)
        sys.stdout.flush()

        logger.info(f"Sending request to OMLX model: {self.model}")
        
        # Prepare content list for multi-modal support
        content = [{"type": "text", "text": prompt}]
        
        if images:
            for img in images:
                if os.path.exists(img):
                    with open(img, "rb") as f:
                        b64_img = base64.b64encode(f.read()).decode('utf-8')
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                        })
                else:
                    # Assume already base64
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img}"}
                    })

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        
        messages.append({"role": "user", "content": content})

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=True
            )
            
            full_response = ""
            chunk_count = 0
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    res_content = chunk.choices[0].delta.content
                    full_response += res_content
                    chunk_count += 1
                    if chunk_count % 5 == 0:
                        sys.stdout.write(".")
                        sys.stdout.flush()
            
            sys.stdout.write(" [Done]\n")
            sys.stdout.flush()
            return full_response
        except Exception as e:
            error_msg = f"Error calling omlx LLM: {e}"
            logger.error(error_msg)
            sys.stdout.write(" [Failed]\n")
            sys.stdout.flush()
            return error_msg
