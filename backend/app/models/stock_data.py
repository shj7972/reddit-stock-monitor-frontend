from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class RedditPost(BaseModel):
    title: str
    score: int
    comments: int
    url: str
    sentiment: float = Field(default=0.0, ge=-1.0, le=1.0)
    keywords: List[str] = Field(default_factory=list)
    created_utc: float
    subreddit: str
    selftext: Optional[str] = None

class StockData(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    sentiment: float = Field(default=0.0, ge=-1.0, le=1.0)
    mentions: int = Field(default=0, ge=0)
    price_change_24h: Optional[float] = None
    key_words: List[str] = Field(default_factory=list)
    posts: List[RedditPost] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class StockDataResponse(BaseModel):
    timestamp: int
    stocks: Dict[str, Dict[str, Any]]
    total_mentions: int
    status: str = "success"

class StockDetailResponse(BaseModel):
    timestamp: int
    ticker: str
    data: Dict[str, Any]
    status: str = "success"