"""Ollama service for handling AI model interactions."""

import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
import json
import logging

from app.core.config import settings
from app.schemas.ollama import ChatRequest, ChatResponse, GenerateRequest, ModelInfo

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama API."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.default_model = settings.OLLAMA_DEFAULT_MODEL

    async def _make_request(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make a request to Ollama API."""
        url = f"{self.base_url}/{endpoint}"

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(
                            f"Ollama API error: {response.status} - {error_text}"
                        )
            except aiohttp.ClientError as e:
                logger.error(f"Failed to connect to Ollama: {e}")
                raise Exception(f"Failed to connect to Ollama: {e}")

    async def chat_with_system(
        self,
        messages: List[dict],
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
    ) -> ChatResponse:
        """Send structured messages (system + user) to Ollama using chat API."""
        model = model or self.default_model

        data = {
            "model": model,
            "messages": messages,  # [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
            "stream": False,
        }

        # Add optional parameters if provided
        if temperature is not None or max_tokens is not None:
            data["options"] = {}
            if temperature is not None:
                data["options"]["temperature"] = temperature
            if max_tokens is not None:
                data["options"]["num_predict"] = max_tokens

        response_data = await self._make_request("api/chat", data)

        return ChatResponse(
            response=response_data.get("message", {}).get("content", ""),
            model=response_data.get("model", model),
            created_at=response_data.get("created_at", ""),
            done=response_data.get("done", True),
            total_duration=response_data.get("total_duration"),
            load_duration=response_data.get("load_duration"),
            prompt_eval_count=response_data.get("prompt_eval_count"),
            prompt_eval_duration=response_data.get("prompt_eval_duration"),
            eval_count=response_data.get("eval_count"),
            eval_duration=response_data.get("eval_duration"),
        )

    async def list_models(self) -> List[ModelInfo]:
        """List available models."""
        response_data = await self._make_request("api/tags", {})

        models = []
        for model_data in response_data.get("models", []):
            models.append(
                ModelInfo(
                    name=model_data.get("name", ""),
                    modified_at=model_data.get("modified_at", ""),
                    size=model_data.get("size", 0),
                    digest=model_data.get("digest", ""),
                )
            )

        return models

    async def health_check(self) -> bool:
        """Check if Ollama service is healthy."""
        try:
            await self._make_request("api/tags", {})
            return True
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False


# Create global service instance
ollama_service = OllamaService()
