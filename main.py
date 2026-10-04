import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base,engine
from .routers import auth,profile,approvals,applications,documents,dashboard,official
from .config import settings
os.makedirs(settings.upload_dir,exist_ok=True)
Base.metadata.create_all(bind=engine)
app=FastAPI(title='CIVIC@ME — Intelligent Industrial Approvals',version='2.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(',')],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
for router in [auth.router,profile.router,approvals.router,applications.router,documents.router,dashboard.router,official.router]: app.include_router(router,prefix='/api')
@app.get('/api/health')
def health(): return {'status':'ok','service':'CIVIC@ME','version':'2.0.0'}
