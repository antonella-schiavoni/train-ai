"""Pydantic schemas for Ollama API endpoints."""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")


class Exercise(BaseModel):
    """Individual exercise model."""

    machine: str = Field(..., description="Gym machine or equipment used")
    exercise_name: str = Field(..., description="Name of the exercise")
    sets: int = Field(..., description="Number of sets")
    reps: int = Field(..., description="Number of repetitions per set")
    duration_minutes: int = Field(..., description="Duration in minutes")
    intensity: Literal["Low", "Medium", "High"] = Field(
        ..., description="Exercise intensity level"
    )


class WorkoutDay(BaseModel):
    """Daily workout routine model."""

    day: str = Field(..., description="Day of the week")
    exercises: List[Exercise] = Field(..., description="List of exercises for this day")


class UserProfile(BaseModel):
    """User profile information."""

    age: int = Field(..., description="Age in years")
    weight: int = Field(..., description="Weight in kilograms")
    height: int = Field(..., description="Height in centimeters")
    physical_condition: str = Field(..., description="Current physical condition")
    training_frequency: int = Field(
        ..., description="Number of training sessions per week"
    )
    workout_time_per_session: int = Field(
        ..., description="Workout duration per session in minutes"
    )


class WorkoutPlan(BaseModel):
    """Complete workout plan response model."""

    user_profile: UserProfile = Field(..., description="User profile information")
    weekly_routine: List[WorkoutDay] = Field(..., description="Weekly workout routine")


class ChatRequest(BaseModel):
    """Request schema for workout chat endpoint."""

    model: Optional[str] = Field(
        None, description="Model to use (defaults to configured model)"
    )
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
    temperature: Optional[float] = Field(
        None, ge=0.0, le=2.0, description="Temperature for response generation"
    )
    max_tokens: Optional[int] = Field(
        None, ge=1, le=4000, description="Maximum tokens in response"
    )
    stream: bool = Field(False, description="Whether to stream the response")

    class Config:
        """Example request schema."""

        schema_extra = {
            "example": {
                "model": "llama3",
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
                "temperature": 0.7,
                "max_tokens": 2000,
            }
        }


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
