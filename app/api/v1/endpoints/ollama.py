"""Ollama API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
import json
import re

from app.schemas.ollama import (
    ChatRequest,
    ChatResponse,
    ModelInfo,
    ModelsResponse,
    ErrorResponse,
    WorkoutPlan,
)
from app.services.ollama import ollama_service
from app.services.agenta import agenta_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ollama", tags=["ollama"])


@router.post("/chat", response_model=WorkoutPlan)
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

        # Template the user message with actual data
        user_template = None
        system_message = None

        # Extract system and user messages from Agenta
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg
            elif msg["role"] == "user":
                user_template = msg["content"]

        if not user_template:
            raise ValueError("No user message template found in Agenta configuration")

        # Use safe string replacement to avoid conflicts with JSON braces
        templated_user_message = user_template

        # Replace template placeholders (use {{variable}} format to avoid JSON conflicts)
        replacements = {
            "{{age}}": str(request.age),
            "{{height}}": str(request.height),
            "{{weight}}": str(request.weight),
            "{{physical_condition}}": request.physical_condition,
            "{{sessions_per_week}}": str(request.sessions_per_week),
            "{{workout_time}}": str(request.workout_time),
            "{{available_machines}}": ", ".join(request.available_machines),
        }

        for placeholder, value in replacements.items():
            templated_user_message = templated_user_message.replace(placeholder, value)

        logger.debug(f"Templated user message: {templated_user_message}")

        # Build final messages array
        final_messages = []
        if system_message:
            final_messages.append(system_message)
        final_messages.append({"role": "user", "content": templated_user_message})

        # Use structured outputs with Pydantic schema
        workout_schema = WorkoutPlan.model_json_schema()

        response = await ollama_service.chat_with_system(
            final_messages,
            request.model,
            request.temperature,
            request.max_tokens,
            format_schema=workout_schema,
        )

        # Parse the JSON response and return as structured data
        try:
            workout_data = json.loads(response.response)
            workout_plan = WorkoutPlan(**workout_data)
            logger.info("Successfully parsed workout plan from Ollama response")
            return workout_plan
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse workout plan JSON: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to parse workout plan from AI response"
            )

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
