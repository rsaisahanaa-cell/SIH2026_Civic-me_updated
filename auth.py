from datetime import datetime,timedelta
import jwt
from passlib.context import CryptContext
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,EmailStr
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..config import settings
router=APIRouter(prefix='/auth',tags=['Authentication']); pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); bearer=HTTPBearer(auto_error=False)
class Login(BaseModel): email:EmailStr; password:str
class Register(BaseModel): name:str; email:EmailStr; password:str; role:str='applicant'
def token(u): return jwt.encode({'sub':str(u.id),'role':u.role,'exp':datetime.utcnow()+timedelta(hours=12)},settings.secret_key,algorithm='HS256')
def current_user(creds=Depends(bearer),db:Session=Depends(get_db)):
 if not creds: raise HTTPException(401,'Authentication required')
 try: p=jwt.decode(creds.credentials,settings.secret_key,algorithms=['HS256']); u=db.get(User,int(p['sub']))
 except Exception: u=None
 if not u: raise HTTPException(401,'Invalid or expired token')
 return u
@router.post('/register')
def register(x:Register,db:Session=Depends(get_db)):
 if db.query(User).filter_by(email=x.email).first(): raise HTTPException(400,'Email already registered')
 if x.role not in ('applicant','official'): x.role='applicant'
 u=User(name=x.name,email=x.email,password_hash=pwd.hash(x.password),role=x.role); db.add(u); db.commit(); db.refresh(u); return {'token':token(u),'user':{'id':u.id,'name':u.name,'email':u.email,'role':u.role}}
@router.post('/login')
def login(x:Login,db:Session=Depends(get_db)):
 u=db.query(User).filter_by(email=x.email).first()
 if not u or not pwd.verify(x.password,u.password_hash): raise HTTPException(401,'Invalid email or password')
 return {'token':token(u),'user':{'id':u.id,'name':u.name,'email':u.email,'role':u.role}}
@router.get('/me')
def me(u=Depends(current_user)): return {'id':u.id,'name':u.name,'email':u.email,'role':u.role}
