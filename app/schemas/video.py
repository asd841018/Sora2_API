from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Any

class VideoCreateRequest(BaseModel):
    text_prompt: str = Field(..., description="Text prompt for video generation", min_length=1)
    image_url: Optional[HttpUrl] = Field(None, description="Optional image URL for image-to-video generation")
    duration: int = Field(12, description="Video duration in seconds", ge=1, le=60)
    generate_audio: bool = Field(False, description="Whether to generate audio")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text_prompt": "A cute cat playing on the grass",
                "image_url": "https://example.com/cat.jpg",
                "duration": 12,
                "generate_audio": False
            }
        }
        
# Response models
class VbenResponse(BaseModel):
    """Vben Admin standard response wrapper."""

    code: int = 0
    message: str = "ok"
    data: Optional[Any] = None