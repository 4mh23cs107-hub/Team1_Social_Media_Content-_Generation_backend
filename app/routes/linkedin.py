from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Content
from ..utils.deps import get_current_user
from ..utils.linkedin_service import linkedin_service
import os

router = APIRouter(prefix="/linkedin", tags=["linkedin"])

@router.get("/login-url")
def get_linkedin_login_url():
    return {"url": linkedin_service.get_authorization_url()}

@router.get("/callback")
def linkedin_callback(code: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")
    
    token_data = linkedin_service.get_access_token(code)
    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail=f"Failed to get access token: {token_data}")
    
    access_token = token_data["access_token"]
    
    # Get profile to get the LinkedIn ID (sub)
    profile = linkedin_service.get_user_profile(access_token)
    linkedin_id = profile.get("sub") or profile.get("id")
    
    if not linkedin_id:
        raise HTTPException(status_code=400, detail="Failed to get LinkedIn Profile ID")
    
    # Update user
    current_user.linkedin_access_token = access_token
    current_user.linkedin_id = linkedin_id
    db.commit()
    
    return {"message": "LinkedIn connected successfully", "profile": profile}

@router.post("/post/{content_id}")
def post_to_linkedin(content_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.linkedin_access_token or not current_user.linkedin_id:
        raise HTTPException(status_code=400, detail="LinkedIn not connected")
    
    content = db.query(Content).filter(Content.id == content_id, Content.author_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Combine text and hashtags
    full_text = f"{content.generated_text}\n\n{content.hashtags}"
    
    response = linkedin_service.post_content(
        access_token=current_user.linkedin_access_token,
        linkedin_id=current_user.linkedin_id,
        text=full_text
    )
    
    if "id" in response:
        content.status = "published"
        db.commit()
        return {"message": "Posted successfully", "linkedin_post_id": response["id"]}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to post: {response}")
