import os
import time  
import logging
from typing import Optional, Dict, Any
from byteplussdkarkruntime import Ark

from app.config import settings


logger = logging.getLogger(__name__)


class VideoGenError(Exception):
    """Base exception class for video generation service"""
    pass


class APIConnectionError(VideoGenError):
    """API connection error"""
    pass


class InvalidParameterError(VideoGenError):
    """Parameter validation error"""
    pass


class VideoGenerationError(VideoGenError):
    """Video generation failed error"""
    pass


class VideoGenService:
    def __init__(self):
        try:
            self.client = Ark(
                base_url="https://ark.ap-southeast.bytepluses.com/api/v3",
                api_key=settings.BYTEDANCE_ARK_API_KEY
            )
            self.model_id = settings.BYTEDANCE_MODEL_ID
            logger.info("VideoGenService initialized successfully")
        except Exception as e:
            logger.error(f"VideoGenService initialization failed: {str(e)}")
            raise APIConnectionError(f"Failed to initialize ByteDance Ark client: {str(e)}")
        
    def create_video(
        self, 
        text_prompt: str, 
        image_url: Optional[str] = None, 
        duration: int = 12, 
        generate_audio: bool = False
    ) -> Dict[str, Any]:
        """
        Create video generation task
        
        Args:
            text_prompt: Text prompt for video generation
            image_url: Optional image URL for image-to-video
            duration: Video duration in seconds
            generate_audio: Whether to generate audio
            
        Returns:
            Creation result
            
        Raises:
            InvalidParameterError: Parameter validation failed
            APIConnectionError: API connection failed
            VideoGenerationError: Video generation failed
        """
        # Parameter validation
        try:
            self._validate_parameters(text_prompt, image_url, duration)
        except ValueError as e:
            logger.error(f"參數驗證失敗: {str(e)}")
            raise InvalidParameterError(str(e))
        
        # Build request content
        try:
            content = self._build_content(text_prompt, image_url)
        except Exception as e:
            logger.error(f"Failed to build request content: {str(e)}")
            raise InvalidParameterError(f"Failed to build request content: {str(e)}")
        
        # Call API to generate video
        try:
            logger.info(f"Starting video task creation - prompt: {text_prompt[:50]}..., duration: {duration}s")
            
            create_result = self.client.content_generation.tasks.create(
                model=self.model_id,
                content=content,
                duration=duration,
                generate_audio=generate_audio
            )
            
            logger.info(f"Video task created successfully - task_id: {getattr(create_result, 'id', 'unknown')}")
            return create_result
            
        except ConnectionError as e:
            logger.error(f"API connection failed: {str(e)}")
            raise APIConnectionError(f"Failed to connect to ByteDance Ark API: {str(e)}")
            
        except TimeoutError as e:
            logger.error(f"API request timeout: {str(e)}")
            raise APIConnectionError(f"API request timeout, please try again later: {str(e)}")
            
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise VideoGenerationError(f"Error occurred during video generation: {str(e)}")
    
    def _validate_parameters(
        self, 
        text_prompt: str, 
        image_url: Optional[str], 
        duration: int
    ) -> None:
        """Validate input parameters"""
        if not text_prompt or not text_prompt.strip():
            raise ValueError("text_prompt cannot be empty")
        
        if len(text_prompt) > 2000:
            raise ValueError(f"text_prompt length cannot exceed 2000 characters, current length: {len(text_prompt)}")
        
        if duration not in [4, 8, 12]:
            raise ValueError(f"duration must be 4, 8, or 12 seconds, current value: {duration}")
        
        if image_url and not (image_url.startswith('http://') or image_url.startswith('https://')):
            raise ValueError(f"image_url must be a valid HTTP/HTTPS URL: {image_url}")
    
    def _build_content(self, text_prompt: str, image_url: Optional[str]) -> list:
        """Build request content"""
        content = [
            {
                "type": "text",
                "text": text_prompt
            }
        ]
        
        if image_url:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            )
        
        return content