from datetime import datetime,timedelta
import secrets
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .auth import current_user
from ..database import get_db
from ..models import Application,Approval,BusinessProfile,WorkflowStep
router=APIRouter(prefix='/applications',tags=['Applications'])
class Create(BaseModel): approval_code:str
@router.get('')
def list_apps(u=Depends(current_user),db:Session=Depends(get_db)):
 apps=db.query(Application).filter_by(user_id=u.id).order_by(Application.created_at.desc()).all(); return [serialize(a,db) for a in apps]
def serialize(a,db):
 steps=db.query(WorkflowStep).filter_by(application_id=a.id).order_by(WorkflowStep.sequence).all()
 return {'id':a.id,'reference':a.reference,'approval_id':a.approval_id,'status':a.status,'submitted_at':a.submitted_at,'due_at':a.due_at,'department':a.department,'query':a.query,'steps':[s.__dict__ for s in steps]}
@router.post('')
def create(x:Create,u=Depends(current_user),db:Session=Depends(get_db)):
 p=db.query(BusinessProfile).filter_by(user_id=u.id).first(); ap=db.query(Approval).filter_by(code=x.approval_code).first()
 if not p: raise HTTPException(400,'Create your business profile first')
 if not ap: raise HTTPException(404,'Approval not found')
 a=Application(reference='CIVIC-'+secrets.token_hex(4).upper(),user_id=u.id,approval_id=ap.id,department=ap.authority); db.add(a); db.flush(); db.add_all([WorkflowStep(application_id=a.id,step_name='Application Intake',department=ap.authority,status='Pending',sequence=1),WorkflowStep(application_id=a.id,step_name='Document Scrutiny',department=ap.authority,status='Pending',sequence=2),WorkflowStep(application_id=a.id,step_name='Inspection / Query',department=ap.authority,status='Pending',sequence=3),WorkflowStep(application_id=a.id,step_name='Decision',department=ap.authority,status='Pending',sequence=4)]); db.commit(); return serialize(a,db)
@router.post('/{app_id}/submit')
def submit(app_id:int,u=Depends(current_user),db:Session=Depends(get_db)):
 a=db.query(Application).filter_by(id=app_id,user_id=u.id).first()
 if not a: raise HTTPException(404,'Application not found')
 ap=db.get(Approval,a.approval_id); now=datetime.utcnow(); a.status='Submitted'; a.submitted_at=now; a.due_at=now+timedelta(days=ap.sla_days)
 steps=db.query(WorkflowStep).filter_by(application_id=a.id).order_by(WorkflowStep.sequence).all()
 if steps: steps[0].status='In Review'; steps[0].started_at=now
 db.commit(); return serialize(a,db)
@router.post('/{app_id}/advance')
def advance(app_id:int,u=Depends(current_user),db:Session=Depends(get_db)):
 a=db.query(Application).filter_by(id=app_id).first()
 if not a: raise HTTPException(404,'Application not found')
 steps=db.query(WorkflowStep).filter_by(application_id=a.id).order_by(WorkflowStep.sequence).all(); cur=next((s for s in steps if s.status=='In Review'),None)
 if cur: cur.status='Completed'; cur.completed_at=datetime.utcnow(); nxt=next((s for s in steps if s.status=='Pending'),None); 
 else: nxt=None
 if nxt: nxt.status='In Review'; nxt.started_at=datetime.utcnow(); a.status='Under Review'
 else: a.status='Approved'; a.query=None
 db.commit(); return serialize(a,db)
