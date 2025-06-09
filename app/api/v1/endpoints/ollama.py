"""Ollama API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from app.schemas.ollama import (
    ChatRequest,
    ChatResponse,
    GenerateRequest,
    ModelInfo,
    ModelsResponse,
    ErrorResponse,
)
from app.services.ollama import ollama_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ollama", tags=["ollama"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a chat message to Ollama.

    - **message**: The user's message
    - **model**: Optional model to use (defaults to configured model)
    - **temperature**: Control randomness (0.0 to 2.0)
    - **max_tokens**: Maximum tokens in response
    - **stream**: Whether to stream the response
    """
    try:
        response = await ollama_service.chat(request)
        return response
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=ChatResponse)
async def generate(request: GenerateRequest):
    """
    Generate text from a prompt using Ollama.

    - **prompt**: The text prompt
    - **model**: Optional model to use (defaults to configured model)
    - **temperature**: Control randomness (0.0 to 2.0)
    - **max_tokens**: Maximum tokens in response
    - **stream**: Whether to stream the response
    """
    try:
        response = await ollama_service.generate(request)
        return response
    except Exception as e:
        logger.error(f"Generate endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models", response_model=ModelsResponse)
async def list_models():
    """
    List all available Ollama models.

    Returns a list of models with their information including:
    - Name
    - Last modified date
    - Size
    - Digest/hash
    """
    try:
        models = await ollama_service.list_models()
        return ModelsResponse(models=models)
    except Exception as e:
        logger.error(f"List models endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Check if Ollama service is healthy and accessible.

    Returns the health status of the Ollama connection.
    """
    try:
        is_healthy = await ollama_service.health_check()
        if is_healthy:
            return {
                "status": "healthy",
                "service": "ollama",
                "message": "Ollama service is accessible",
            }
        else:
            raise HTTPException(
                status_code=503, detail="Ollama service is not accessible"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
