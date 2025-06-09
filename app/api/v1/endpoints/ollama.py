"""Ollama API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from app.schemas.ollama import (
    ChatRequest,
    ChatResponse,
    ModelInfo,
    ModelsResponse,
    ErrorResponse,
)
from app.services.ollama import ollama_service
from app.services.agenta import agenta_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ollama", tags=["ollama"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate a workout plan based on user parameters.

    - **age**: Age in years
    - **height**: Height in centimeters
    - **weight**: Weight in kilograms
    - **physical_condition**: Current physical condition
    - **sessions_per_week**: Number of workout sessions per week
    - **workout_time**: Workout duration in minutes
    - **available_machines**: List of available gym machines/equipment
    - **model**: Optional model to use (defaults to configured model)
    - **temperature**: Control randomness (0.0 to 2.0)
    - **max_tokens**: Maximum tokens in response
    - **stream**: Whether to stream the response
    """
    try:
        # Get structured messages from Agenta
        messages = await agenta_service.get_messages()

        # Construct user message from workout parameters
        machines_list = ", ".join(request.available_machines)
        user_message = f"""
Please create a personalized workout plan with the following specifications:

- Age: {request.age} years
- Height: {request.height} cm
- Weight: {request.weight} kg
- Physical condition: {request.physical_condition}
- Sessions per week: {request.sessions_per_week}
- Workout duration: {request.workout_time} minutes

Available machines/equipment:
{machines_list}

Please provide a detailed workout plan that includes exercises, sets, reps, and rest periods.
""".strip()

        # Add user message to the conversation
        messages.append({"role": "user", "content": user_message})

        response = await ollama_service.chat_with_system(
            messages, request.model, request.temperature, request.max_tokens
        )
        return response
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
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
