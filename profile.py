from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .auth import current_user
from ..database import get_db
from ..models import BusinessProfile
router=APIRouter(prefix='/profile',tags=['Business Profile'])
class ProfileIn(BaseModel): name:str; sector:str; location:str='Maharashtra'; project_size:str='Medium'; stage:str='New'; employees:int=20
@router.get('')
def get_profile(u=Depends(current_user),db:Session=Depends(get_db)):
 p=db.query(BusinessProfile).filter_by(user_id=u.id).first(); return p.__dict__ if p else None
@router.post('')
def save_profile(x:ProfileIn,u=Depends(current_user),db:Session=Depends(get_db)):
 p=db.query(BusinessProfile).filter_by(user_id=u.id).first()
 if not p: p=BusinessProfile(user_id=u.id,**x.model_dump()); db.add(p)
 else:
  for k,v in x.model_dump().items(): setattr(p,k,v)
 db.commit(); db.refresh(p); return p.__dict__
