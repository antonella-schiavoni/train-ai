"""Pydantic schemas for Ollama API endpoints."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(..., description="User message")
    model: Optional[str] = Field(
        None, description="Model to use (defaults to configured model)"
    )
    temperature: Optional[float] = Field(
        None, ge=0.0, le=2.0, description="Temperature for response generation"
    )
    max_tokens: Optional[int] = Field(
        None, ge=1, le=4000, description="Maximum tokens in response"
    )
    stream: bool = Field(False, description="Whether to stream the response")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str = Field(..., description="Generated response")
    model: str = Field(..., description="Model used for generation")
    created_at: str = Field(..., description="Response creation timestamp")
    done: bool = Field(..., description="Whether the response is complete")
    total_duration: Optional[int] = Field(
        None, description="Total processing duration in nanoseconds"
    )
    load_duration: Optional[int] = Field(
        None, description="Model loading duration in nanoseconds"
    )
    prompt_eval_count: Optional[int] = Field(
        None, description="Number of tokens in the prompt"
    )
    prompt_eval_duration: Optional[int] = Field(
        None, description="Prompt evaluation duration in nanoseconds"
    )
    eval_count: Optional[int] = Field(
        None, description="Number of tokens in the response"
    )
    eval_duration: Optional[int] = Field(
        None, description="Response generation duration in nanoseconds"
    )


class GenerateRequest(BaseModel):
    """Request schema for workout generation endpoint."""

    age: int = Field(..., description="Age in years")
    height: int = Field(..., description="Height in centimeters")
    weight: int = Field(..., description="Weight in kilograms")
    physical_condition: str = Field(..., description="Current physical condition")
    sessions_per_week: int = Field(
        ..., description="Number of workout sessions per week"
    )
    workout_time: int = Field(..., description="Workout duration in minutes")
    available_machines: List[str] = Field(
        ..., description="List of available gym machines/equipment"
    )

    class Config:
        """Example request schema."""

        schema_extra = {
            "example": {
                "age": 32,
                "height": 165,
                "weight": 92,
                "physical_condition": "overweight",
                "sessions_per_week": 3,
                "workout_time": 90,
                "available_machines": [
                    "rear kick",
                    "hip trust",
                    "leg standing curl",
                ],
            }
        }


class ModelInfo(BaseModel):
    """Model information schema."""

    name: str = Field(..., description="Model name")
    modified_at: str = Field(..., description="Last modification timestamp")
    size: int = Field(..., description="Model size in bytes")
    digest: str = Field(..., description="Model digest/hash")


class ModelsResponse(BaseModel):
    """Response schema for models list endpoint."""

    models: List[ModelInfo] = Field(..., description="List of available models")


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
