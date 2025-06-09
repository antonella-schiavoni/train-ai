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
    """Request schema for generate endpoint."""

    prompt: str = Field(..., description="Text prompt")
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
