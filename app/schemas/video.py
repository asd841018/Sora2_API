from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Any, List, Literal

# Content types for the request

class VideoCreateRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for video generation")
    image_url: Optional[str] = Field(None, description="Optional image URL for video generation")
    
    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "model": "ep-20260129105436-445p4",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": "At breakneck speed, drones thread through intricate obstacles --duration 5"
    #                 },
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {
    #                         "url": "https://example.com/image.png"
    #                     }
    #                 }
    #             ]
    #         }
    #     }

# Task response model
class TaskResponse(BaseModel):
    id: str = Field(..., description="Task ID")
    model: str = Field(..., description="Model ID")
    status: str = Field(..., description="Task status: pending, processing, completed, failed")
    created_at: int = Field(..., description="Creation timestamp")
    updated_at: Optional[int] = Field(None, description="Update timestamp")
    result: Optional[Any] = Field(None, description="Generation result (available when completed)")
    error: Optional[str] = Field(None, description="Error message (available when failed)")

# Response models
class VbenResponse(BaseModel):
    """Vben Admin standard response wrapper."""

    code: int = 0
    message: str = "ok"
    data: Optional[Any] = None