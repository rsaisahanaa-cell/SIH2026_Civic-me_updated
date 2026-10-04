import os,uuid
from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from .auth import current_user
from ..database import get_db
from ..models import Application,Document,Approval
from ..config import settings
router=APIRouter(prefix='/documents',tags=['Documents'])
ALLOWED={'.pdf','.png','.jpg','.jpeg','.doc','.docx','.xlsx'}
@router.get('/{app_id}')
def docs(app_id:int,u=Depends(current_user),db:Session=Depends(get_db)):
 a=db.query(Application).filter_by(id=app_id,user_id=u.id).first()
 if not a: raise HTTPException(404,'Application not found')
 return [d.__dict__ for d in db.query(Document).filter_by(application_id=app_id).all()]
@router.post('/{app_id}/upload')
async def upload(app_id:int,file:UploadFile=File(...),u=Depends(current_user),db:Session=Depends(get_db)):
 a=db.query(Application).filter_by(id=app_id,user_id=u.id).first()
 if not a: raise HTTPException(404,'Application not found')
 ext=os.path.splitext(file.filename or '')[1].lower()
 if ext not in ALLOWED: raise HTTPException(400,'Unsupported document type')
 data=await file.read()
 if len(data)>10*1024*1024: raise HTTPException(400,'Maximum file size is 10 MB')
 stored=f'{uuid.uuid4().hex}{ext}'; path=os.path.join(settings.upload_dir,stored)
 with open(path,'wb') as f:f.write(data)
 score=100.0 if len(data)>500 else 75.0
 d=Document(application_id=app_id,original_name=file.filename,stored_name=stored,mime_type=file.content_type or 'application/octet-stream',size_bytes=len(data),validation_score=score,validation_notes='Uploaded successfully; format and file-size pre-check passed.')
 db.add(d); db.commit(); db.refresh(d); return d.__dict__
