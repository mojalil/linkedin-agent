from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ContentItem(BaseModel):
    """Represents a single piece of content from any source."""
    title: str
    url: str
    source: str  # "youtube", "twitter", or "web"
    engagement_score: float = Field(default=0.0, ge=0.0, le=1.0)
    published_at: datetime
    content: str
    metadata: dict = Field(default_factory=dict)

class ScrapedContent(BaseModel):
    """Collection of scraped content from all sources."""
    youtube_content: List[ContentItem] = Field(default_factory=list)
    twitter_content: List[ContentItem] = Field(default_factory=list)
    web_content: List[ContentItem] = Field(default_factory=list)

class BlogPost(BaseModel):
    """Represents the final blog post to be published."""
    title: str
    content: str
    hero_image_url: Optional[str] = None
    references: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

class AgentState(BaseModel):
    """Global state for the LangGraph system."""
    topic: str
    scraped_content: ScrapedContent = Field(default_factory=ScrapedContent)
    blog_post: Optional[BlogPost] = None
    current_step: str = "planning"
    error: Optional[str] = None
    metadata: dict = Field(default_factory=dict) 