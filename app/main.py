"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.core.config import settings

# Create FastAPI app using settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI application for AI/ML services",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
)

# Add CORS middleware using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "version": settings.VERSION,
        "docs": "/docs",
        "debug_mode": settings.DEBUG,
        "environment": "development" if settings.DEBUG else "production",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
    }


@app.get("/config")
async def get_config():
    """Get current configuration (non-sensitive values only)."""
    return {
        "host": settings.HOST,
        "port": settings.PORT,
        "debug": settings.DEBUG,
        "model_path": settings.MODEL_PATH,
        "max_batch_size": settings.MAX_BATCH_SIZE,
        "upload_dir": settings.UPLOAD_DIR,
        "log_level": settings.LOG_LEVEL,
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
