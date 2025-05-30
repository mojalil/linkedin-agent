from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    apify_token: str
    firecrawl_token: str
    linkedin_access_token: str
    linkedin_member_id: str
    openai_api_key: str
    
    # API Configuration
    openai_model: str = "gpt-4-turbo-preview"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # Scraping Configuration
    max_web_results: int = 10
    max_youtube_results: int = 5
    max_twitter_results: int = 5
    
    # Content Generation
    min_engagement_score: float = 0.5
    max_references: int = 5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 