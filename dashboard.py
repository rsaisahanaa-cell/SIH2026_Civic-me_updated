from datetime import datetime
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .auth import current_user
from ..database import get_db
from ..models import Application,Document,Renewal,Incentive,BusinessProfile
router=APIRouter(prefix='/dashboard',tags=['Dashboard'])
@router.get('')
def dashboard(u=Depends(current_user),db:Session=Depends(get_db)):
 apps=db.query(Application).filter_by(user_id=u.id).all(); docs=sum(len(db.query(Document).filter_by(application_id=a.id).all()) for a in apps); due=[a for a in apps if a.due_at and a.status not in ('Approved','Rejected')]
 return {'role':u.role,'profile':db.query(BusinessProfile).filter_by(user_id=u.id).first() is not None,'metrics':{'applications':len(apps),'in_review':sum(a.status in ('Submitted','Under Review') for a in apps),'approved':sum(a.status=='Approved' for a in apps),'documents':docs,'sla_at_risk':sum(a.due_at and (a.due_at-datetime.utcnow()).total_seconds()<3*86400 and a.status!='Approved' for a in due)},'renewals':[r.__dict__ for r in db.query(Renewal).filter_by(user_id=u.id).all()],'incentives':[i.__dict__ for i in db.query(Incentive).limit(10).all()]}
