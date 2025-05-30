from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # API Keys
    apify_token: str
    firecrawl_token: str
    linkedin_access_token: str
    linkedin_member_id: str
    openai_api_key: str

    # API Configuration
    openai_model: str = "gpt-4"
    max_links_per_source: int = 20
    max_top_links: int = 6
    
    # Content Settings
    blog_word_count: int = 1000
    image_size: str = "1024x1024"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Create a global settings instance
settings = get_settings()
