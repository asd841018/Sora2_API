from fastapi import APIRouter, HTTPException, status, Path
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

from app.schemas.video import VideoCreateRequest, VbenResponse, TaskResponse
from app.services.video_gen import VideoGenService, APIConnectionError, InvalidParameterError, VideoGenerationError

# Create router
router = APIRouter(prefix="/api/v1/videos", tags=["Videos"])

# Initialize service
video_service = VideoGenService()

@router.post("/tasks", response_model=VbenResponse, status_code=status.HTTP_201_CREATED)
async def create_video_task(request: VideoCreateRequest):
    """
    Create video generation task
    
    - **model**: Model ID (e.g., "ep-20260129105436-445p4")
    - **content**: Content array with text and optional image
        - Text content: {"type": "text", "text": "your prompt --duration 5"}
        - Image content: {"type": "image_url", "image_url": {"url": "https://..."}}
    
    Returns:
        Task ID and creation info
    """
    try:
        # Convert Pydantic models to dict for the service
        content_list = []
        if not request.prompt:
            raise InvalidParameterError("Prompt cannot be empty")
        
        content_list.append({
            "type": "text",
            "text": request.prompt
        })
        if request.image_url:
            content_list.append({
                "type": "image_url",
                "image_url": {
                    "url": str(request.image_url)
                }
            })
        
        # Call service to create task
        result = await video_service.create_video_task(
            content=content_list
        )
        
        return VbenResponse(
            code=0,
            message="Video generation task created successfully",
            data=result
        )
        
    except InvalidParameterError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except APIConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except VideoGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/tasks/{task_id}", response_model=VbenResponse)
async def query_video_task(
    task_id: str = Path(..., description="Task ID returned from create task endpoint")
):
    """
    Query video generation task status
    
    - **task_id**: Task ID from the create task response
    
    Returns:
        Task status, progress, and result (if completed)
    """
    try:
        # Call service to query task
        result = await video_service.query_task(task_id)
        
        return VbenResponse(
            code=0,
            message="Task query successful",
            data=result
        )
        
    except APIConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except VideoGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
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
