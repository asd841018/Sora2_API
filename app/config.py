from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using pydantic BaseSettings."""

    # OpenAI API Key
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    
    # ByteDance Ark API Key
    BYTEDANCE_ARK_API_KEY: str = Field(..., env="BYTEDANCE_ARK_API_KEY")
    BYTEDANCE_MODEL_ID: str = Field(..., env="BYTEDANCE_MODEL_ID")
    
     # Environment
    ENV: str = Field(default="dev", description="Environment")
    
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment (development, staging, production)",
    )
    DEBUG: bool = Field(default=True, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Log level")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()