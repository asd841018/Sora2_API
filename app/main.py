import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utils.logger import setup_logging
from app.api.router import router as video_router

# Setup logging
setup_logging(settings)
logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title="Sora2 Video Generation API",
    description="Video generation API based on ByteDance Ark",
    version="1.0.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(video_router)


@app.get("/")
async def root():
    """Root path"""
    return {
        "message": "Welcome to Sora2 Video Generation API",
        "docs": "/docs",
        "health": "/api/v1/videos/health"
    }


@app.get("/health")
async def health():
    """Overall health check"""
    return {"status": "healthy", "message": "API is running normally"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)