from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import Campaign, User
from ..schemas import content_schemas
from ..utils.deps import get_current_user

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.post("/", response_model=content_schemas.Campaign)
def create_campaign(request: content_schemas.CampaignCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_campaign = Campaign(
        title=request.title,
        description=request.description,
        start_date=request.start_date,
        end_date=request.end_date,
        owner_id=current_user.id
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@router.get("/", response_model=List[content_schemas.Campaign])
def list_campaigns(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Campaign).filter(Campaign.owner_id == current_user.id).all()

@router.get("/{campaign_id}", response_model=content_schemas.Campaign)
def get_campaign(campaign_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.owner_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{campaign_id}", response_model=content_schemas.Campaign)
def update_campaign(campaign_id: int, request: content_schemas.CampaignCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.owner_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign.title = request.title
    campaign.description = request.description
    campaign.start_date = request.start_date
    campaign.end_date = request.end_date
    
    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.owner_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return {"message": "Campaign deleted successfully"}
