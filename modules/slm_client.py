# modules/slm_client.py
import logging
import os
import json
import asyncio
from typing import Optional
import httpx
from fastapi import HTTPException

from modules.text_utils import truncate_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SLMClient:
    """
    Client for interacting with a Small Language Model (SLM).
    
    This is a mock implementation that returns placeholder responses.
    Replace with actual API calls when SLM endpoint is available.
    
    To enable real SLM:
    1. Set environment variable: SLM_ENDPOINT_URL
    2. Optionally set: SLM_API_KEY, SLM_MODEL_NAME
    3. Replace mock methods with actual HTTP calls (using httpx or similar)
    """
    
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        """
        Initialize SLM client.
        
        Args:
            endpoint_url: SLM API endpoint (e.g., Groq, vLLM server)
            api_key: API key for authentication
            model_name: Model identifier
        """
        self.endpoint_url = endpoint_url or os.getenv("SLM_ENDPOINT_URL")
        self.api_key = api_key or os.getenv("SLM_API_KEY")
        self.model_name = model_name or os.getenv("SLM_MODEL_NAME", "default-slm")
        
        if self.endpoint_url:
            logger.info(f"SLMClient initialized with endpoint: {self.endpoint_url}")
        else:
            logger.warning("SLMClient running in MOCK mode (no endpoint configured)")
            
        # Initialize persistent client for production use (connection pooling)
        self.client = httpx.AsyncClient(
            timeout=12.0,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=5)
        )
        
    async def aclose(self):
        """Close the persistent HTTP client."""
        await self.client.aclose()
    
    async def generate_chat(
        self,
        message: str,
        language: str = "en",
        user_name: Optional[str] = None,
    ) -> str:
        """
        Generate a direct chat response (no RAG context).
        
        Args:
            message: User's message
            language: Target language for response
            user_name: User's name for personalization
            
        Returns:
            Generated response text
        """
        logger.info(f"SLM generate_chat called - Message: '{message[:50]}...', Language: {language}")
        
        if self.endpoint_url:
            # Real API call to SLM endpoint
            try:
                # Prepare request payload matching SLM API format
                payload = {
                    "question": message,  # SLM expects "question" not "message"
                    "chat_history": "",   # Empty for direct chat
                    "max_tokens": 300,    # limit output for faster generation
                }
                
                # Prepare headers
                headers = {"Content-Type": "application/json"}
                if self.api_key and self.api_key != "your-api-key-if-needed":
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                logger.info(f"Sending request to SLM endpoint: {self.endpoint_url}")
                logger.info(f"Payload: {payload}")
                
                response = await self.client.post(
                    self.endpoint_url,
                    json=payload,
                    headers=headers,
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Extract response text (SLM returns {"reply": "..."})
                if isinstance(result, dict):
                    response_text = result.get("reply") or result.get("response") or result.get("text") or result.get("message") or str(result)
                else:
                    response_text = str(result)
                
                # Truncate response to maximum 2000 characters
                response_text = truncate_response(response_text)
                
                logger.info(f"SLM response received: {response_text[:100]}...")
                return response_text
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"SLM API error: {e.response.status_code} - {e.response.text}")
                raise HTTPException(status_code=502, detail=f"SLM API error: {e.response.status_code}")
            except httpx.TimeoutException:
                logger.error("SLM API timeout")
                raise HTTPException(status_code=504, detail="SLM API timeout")
            except Exception as e:
                logger.error(f"Error calling SLM API: {e}")
                raise HTTPException(status_code=500, detail=f"Error calling SLM: {str(e)}")
        
        # Mock implementation (fallback if no endpoint)
        greeting = f"Hi {user_name}! " if user_name else "Hi! "
        mock_response = (
            f"{greeting}This is a mock SLM response for direct chat. "
            f"You said: '{message}'. "
            f"In production, this would be generated by the Small Language Model. "
            f"[Language: {language}]"
        )
        
        # Truncate response to maximum 2000 characters
        mock_response = truncate_response(mock_response)
        
        logger.info(f"SLM mock response: {mock_response[:100]}...")
        return mock_response
    
    async def generate_rag_response(
        self,
        context: str,
        message: str,
        language: str = "en",
        user_name: Optional[str] = None,
    ) -> str:
        """
        Generate a RAG-enhanced response (non-streaming).
        """
        logger.info(f"SLM generate_rag_response called - Message: '{message[:50]}...', Language: {language}")
        
        if self.endpoint_url:
            try:
                payload = {
                    "question": message,
                    "chat_history": "",
                    "context": context,
                    "max_tokens": 500,
                }
                headers = {"Content-Type": "application/json"}
                if self.api_key and self.api_key != "your-api-key-if-needed":
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                response = await self.client.post(self.endpoint_url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                if isinstance(result, dict):
                    response_text = result.get("reply") or result.get("response") or result.get("text") or str(result)
                else:
                    response_text = str(result)
                
                return truncate_response(response_text)
            except Exception as e:
                logger.error(f"Error in SLM RAG: {e}")
                raise HTTPException(status_code=500, detail=f"SLM RAG failed: {e}")
        
        # Mock fallback
        greeting = f"Hello {user_name}, " if user_name else "Hello, "
        return f"{greeting}this is a mock non-streaming RAG response. Context: {len(context)} chars."

    async def stream_generate(
        self,
        message: str,
        language: str = "en",
        user_name: Optional[str] = None,
    ):
        """
        Stream a direct chat response (no RAG context).
        Yields chunks of text.
        """
        logger.info(f"SLM stream_generate called - Message: '{message[:50]}...', Language: {language}")
        
        if self.endpoint_url:
            try:
                payload = {
                    "question": message,
                    "chat_history": "",
                    "max_tokens": 500,
                    "stream": True,
                }
                headers = {"Content-Type": "application/json"}
                if self.api_key and self.api_key != "your-api-key-if-needed":
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with self.client.stream("POST", self.endpoint_url, json=payload, headers=headers) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        # Handling standard Server-Sent Events (SSE) data format
                        if line.startswith("data: "):
                            line = line[6:]
                        if line == "[DONE]":
                            break
                        try:
                            data = json.loads(line)
                            yield data.get("reply") or data.get("response") or data.get("text") or ""
                        except json.JSONDecodeError:
                            yield line
            except Exception as e:
                logger.error(f"Error in SLM stream: {e}")
                yield f"Error: {e}"
                return

        else:
            # Mock Streaming
            greeting = f"Hi {user_name}! " if user_name else "Hi! "
            full_mock = f"{greeting}This is a mock streaming SLM response. You said: '{message}'. [Language: {language}]"
            # Simulate streaming by yielding words
            for word in full_mock.split(" "):
                yield word + " "
                await asyncio.sleep(0.05)

    async def stream_rag_response(
        self,
        context: str,
        message: str,
        language: str = "en",
        user_name: Optional[str] = None,
    ):
        """
        Stream a RAG-enhanced response.
        Yields chunks of text.
        """
        logger.info(f"SLM stream_rag_response called - Message: '{message[:50]}...', Language: {language}")
        
        if self.endpoint_url:
            try:
                payload = {
                    "question": message,
                    "chat_history": "",
                    "context": context,
                    "max_tokens": 500,
                    "stream": True,
                }
                headers = {"Content-Type": "application/json"}
                if self.api_key and self.api_key != "your-api-key-if-needed":
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with self.client.stream("POST", self.endpoint_url, json=payload, headers=headers) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        if line.startswith("data: "):
                            line = line[6:]
                        if line == "[DONE]":
                            break
                        try:
                            data = json.loads(line)
                            yield data.get("reply") or data.get("response") or data.get("text") or ""
                        except json.JSONDecodeError:
                            yield line
            except Exception as e:
                logger.error(f"Error in SLM RAG stream: {e}")
                yield f"Error: {e}"
                return

        else:
            # Mock Streaming
            greeting = f"Hello {user_name}, " if user_name else "Hello, "
            full_mock = f"{greeting}this is a mock SLM RAG streaming response. You said: '{message}'. Context used: {len(context)} chars."
            for word in full_mock.split(" "):
                yield word + " "
                await asyncio.sleep(0.05)

    def is_mock(self) -> bool:
        """
        Check if client is running in mock mode.
        
        Returns:
            True if no endpoint configured (mock mode), False otherwise
        """
        return self.endpoint_url is None


# Module-level singleton instance
_slm_client_instance = None


def get_slm_client() -> SLMClient:
    """
    Get or create a singleton SLMClient instance.
    
    Returns:
        SLMClient instance
    """
    global _slm_client_instance
    if _slm_client_instance is None:
        _slm_client_instance = SLMClient()
    return _slm_client_instance
