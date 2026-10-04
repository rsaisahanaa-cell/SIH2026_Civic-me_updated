from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .auth import current_user
from ..database import get_db
from ..models import BusinessProfile
from ..rules import applicable
router=APIRouter(prefix='/approvals',tags=['Approval Mapper'])
@router.get('/map')
def map_approvals(u=Depends(current_user),db:Session=Depends(get_db)):
 p=db.query(BusinessProfile).filter_by(user_id=u.id).first()
 if not p: return {'profile_required':True,'approvals':[]}
 return {'profile_required':False,'profile':p.__dict__,'approvals':applicable(p)}
