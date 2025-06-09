"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import ollama

# Create the main API v1 router
router = APIRouter(prefix="/api/v1")

# Include endpoint routers
router.include_router(ollama.router)
