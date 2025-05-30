from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class Link(BaseModel):
    """Represents a content link from any source."""
    url: HttpUrl
    title: str
    source: str  # "web" | "youtube" | "twitter"
    views: int
    posted_at: datetime

class FlowState(BaseModel):
    """Main state object that flows through the LangGraph."""
    topic: str
    links: List[Link] = []
    top_links: List[Link] = []
    blog_markdown: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    linkedin_post_url: Optional[HttpUrl] = None
    error: Optional[str] = None
    status: str = "initialized"  # "initialized" | "running" | "completed" | "failed"
