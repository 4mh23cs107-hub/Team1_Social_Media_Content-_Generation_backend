from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContentBase(BaseModel):
    topic: str
    platform: str
    content_type: str
    campaign_id: Optional[int] = None

class ContentCreate(ContentBase):
    pass

class ContentGenerate(BaseModel):
    topic: str
    platform: str
    tone: Optional[str] = "professional"
    target_audience: Optional[str] = "business professionals"

class ContentResponse(ContentBase):
    id: int
    generated_text: str
    hashtags: Optional[str]
    image_url: Optional[str]
    status: str
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CampaignBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
