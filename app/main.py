from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base
from . import models
from .routes import auth, content, campaigns, linkedin

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media Content Generation API",
    description="A comprehensive backend for AI-powered social media content generation.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(campaigns.router)
app.include_router(linkedin.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Social Media Content Generation API", "docs": "/docs"}
