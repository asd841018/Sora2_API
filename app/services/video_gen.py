import os
import time  
import logging
from typing import Optional, Dict, Any, List
import httpx

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
            self.base_url = "https://ark.ap-southeast.bytepluses.com/api/v3"
            self.api_key = settings.BYTEDANCE_ARK_API_KEY
            self.model_id = settings.BYTEDANCE_MODEL_ID
            logger.info("VideoGenService initialized successfully")
        except Exception as e:
            logger.error(f"VideoGenService initialization failed: {str(e)}")
            raise APIConnectionError(f"Failed to initialize ByteDance Ark client: {str(e)}")
        
    async def create_video_task(
        self, 
        content: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create video generation task
        
        Args:
            model: Model ID
            content: Content array with text and optional image
            
        Returns:
            Task creation result with task ID
            
        Raises:
            InvalidParameterError: Parameter validation failed
            APIConnectionError: API connection failed
            VideoGenerationError: Video generation failed
        """
        # Parameter validation
        try:
            self._validate_parameters(content)
        except ValueError as e:
            logger.error(f"Parameter validation failed: {str(e)}")
            raise InvalidParameterError(str(e))
        
        # Call API to create task
        try:
            logger.info(f"Starting video task creation - model: {self.model_id}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/contents/generations/tasks",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    json={
                        "model": self.model_id,
                        "content": content
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
            logger.info(f"Video task created successfully - task_id: {result.get('id', 'unknown')}")
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
            raise APIConnectionError(f"API request failed: {e.response.text}")
            
        except httpx.TimeoutException as e:
            logger.error(f"API request timeout: {str(e)}")
            raise APIConnectionError(f"API request timeout, please try again later: {str(e)}")
            
        except Exception as e:
            logger.error(f"Video task creation failed: {str(e)}")
            raise VideoGenerationError(f"Error occurred during video task creation: {str(e)}")
    
    async def query_task(self, task_id: str) -> Dict[str, Any]:
        """
        Query video generation task status
        
        Args:
            task_id: Task ID
            
        Returns:
            Task status and result
            
        Raises:
            APIConnectionError: API connection failed
            VideoGenerationError: Query failed
        """
        try:
            logger.info(f"Querying task status - task_id: {task_id}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/contents/generations/tasks/{task_id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
            logger.info(f"Task query successful - task_id: {task_id}, status: {result.get('status', 'unknown')}")
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
            raise APIConnectionError(f"API request failed: {e.response.text}")
            
        except httpx.TimeoutException as e:
            logger.error(f"API request timeout: {str(e)}")
            raise APIConnectionError(f"API request timeout, please try again later: {str(e)}")
            
        except Exception as e:
            logger.error(f"Task query failed: {str(e)}")
            raise VideoGenerationError(f"Error occurred during task query: {str(e)}")
    
    def _validate_parameters(self, content: List[Dict[str, Any]]) -> None:
        """Validate input parameters"""
        if not content or len(content) == 0:
            raise ValueError("content cannot be empty")
        
        # Check if there's at least one text content
        has_text = any(item.get("type") == "text" for item in content)
        if not has_text:
            raise ValueError("content must contain at least one text item")
        
        # Validate each content item
        for item in content:
            if item.get("type") == "text":
                text = item.get("text", "")
                if not text or not text.strip():
                    raise ValueError("text content cannot be empty")
                if len(text) > 2000:
                    raise ValueError(f"text length cannot exceed 2000 characters, current length: {len(text)}")
            
            elif item.get("type") == "image_url":
                image_url = item.get("image_url", {}).get("url", "")
                if image_url:
                    if not (image_url.startswith('http://') or image_url.startswith('https://')):
                        raise ValueError(f"image_url must be a valid HTTP/HTTPS URL: {image_url}")