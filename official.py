from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from .auth import current_user
from ..database import get_db
from ..models import Application,User,WorkflowStep
router=APIRouter(prefix='/official',tags=['Official Dashboard'])
def guard(u):
 if u.role!='official': raise HTTPException(403,'Official role required')
@router.get('/dashboard')
def off(u=Depends(current_user),db:Session=Depends(get_db)):
 guard(u); apps=db.query(Application).all(); return {'total':len(apps),'submitted':sum(a.status=='Submitted' for a in apps),'under_review':sum(a.status=='Under Review' for a in apps),'approved':sum(a.status=='Approved' for a in apps),'sla_at_risk':sum(a.due_at and a.status not in ('Approved','Rejected') and (a.due_at-datetime.utcnow()).total_seconds()<3*86400 for a in apps),'applications':[{'id':a.id,'reference':a.reference,'status':a.status,'department':a.department,'due_at':a.due_at,'user_id':a.user_id} for a in apps]}
@router.post('/applications/{app_id}/advance')
def off_advance(app_id:int,u=Depends(current_user),db:Session=Depends(get_db)):
 guard(u); a=db.get(Application,app_id)
 if not a: raise HTTPException(404,'Application not found')
 steps=db.query(WorkflowStep).filter_by(application_id=a.id).order_by(WorkflowStep.sequence).all(); cur=next((s for s in steps if s.status=='In Review'),None); now=datetime.utcnow()
 if cur: cur.status='Completed'; cur.completed_at=now
 nxt=next((s for s in steps if s.status=='Pending'),None)
 if nxt: nxt.status='In Review'; nxt.started_at=now; a.status='Under Review'
 else: a.status='Approved'
 db.commit(); return {'status':a.status}
