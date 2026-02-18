from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import Content, User
from ..schemas import content_schemas
from ..utils.deps import get_current_user
from ..utils.ai_service import generate_social_media_content

router = APIRouter(prefix="/content", tags=["content"])

@router.post("/generate", response_model=content_schemas.ContentResponse)
def generate_content(request: content_schemas.ContentGenerate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Call AI Service
    ai_output = generate_social_media_content(
        topic=request.topic,
        platform=request.platform,
        tone=request.tone,
        audience=request.target_audience
    )
    
    new_content = Content(
        topic=request.topic,
        platform=request.platform,
        content_type="post",
        generated_text=ai_output,
        author_id=current_user.id,
        status="draft"
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content

@router.get("/", response_model=List[content_schemas.ContentResponse])
def list_content(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Content).filter(Content.author_id == current_user.id).all()

@router.get("/{content_id}", response_model=content_schemas.ContentResponse)
def get_content(content_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id, Content.author_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.delete("/{content_id}")
def delete_content(content_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id, Content.author_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
    return {"message": "Content deleted successfully"}
