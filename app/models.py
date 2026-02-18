from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "team1_users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)

    campaigns = relationship("Campaign", back_populates="owner")
    contents = relationship("Content", back_populates="author")

class Campaign(Base):
    __tablename__ = "team1_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("team1_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="campaigns")
    contents = relationship("Content", back_populates="campaign")

class Content(Base):
    __tablename__ = "team1_contents"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    platform = Column(String) # e.g., Instagram, Twitter, LinkedIn
    content_type = Column(String) # e.g., Post, Story, Thread
    generated_text = Column(Text)
    hashtags = Column(Text)
    image_url = Column(String, nullable=True)
    status = Column(String, default="draft") # draft, approved, published
    campaign_id = Column(Integer, ForeignKey("team1_campaigns.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("team1_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="contents")
    author = relationship("User", back_populates="contents")
