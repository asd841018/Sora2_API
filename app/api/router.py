from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

from app.schemas.video import VideoCreateRequest, VbenResponse
from app.services.video_gen import VideoGenService

# 創建 router
router = APIRouter(prefix="/api/v1/videos", tags=["Videos"])

# 初始化服務
video_service = VideoGenService()

@router.post("/generate", response_model=VbenResponse, status_code=status.HTTP_201_CREATED)
def generate_video(request: VideoCreateRequest):
    """
    Create video generation task
    
    - **text_prompt**: Text prompt (required)
    - **image_url**: Optional image URL for image-to-video generation
    - **duration**: Video duration, default 12 seconds
    - **generate_audio**: Whether to generate audio, default False
    """
    try:
        # Call service to generate video
        result = video_service.create_video(
            text_prompt=request.text_prompt,
            image_url=str(request.image_url) if request.image_url else None,
            duration=request.duration,
            generate_audio=request.generate_audio
        )
        
        return VbenResponse(
            code=0,
            message="Video generation task created",
            data=result
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video generation failed: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if video generation service is running normally"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "video_generation",
        "message": "Service is running normally"
    }
