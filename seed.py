from datetime import datetime,timedelta
from passlib.context import CryptContext
from .app.database import Base,engine,SessionLocal
from .app.models import User,Approval,Incentive,Renewal
from .app.rules import RULES
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); Base.metadata.create_all(bind=engine); db=SessionLocal()
if not db.query(User).filter_by(email='demo@civicme.in').first(): db.add(User(name='Demo Entrepreneur',email='demo@civicme.in',password_hash=pwd.hash('Demo@123'),role='applicant'))
if not db.query(User).filter_by(email='official@civicme.in').first(): db.add(User(name='Demo Officer',email='official@civicme.in',password_hash=pwd.hash('Officer@123'),role='official'))
for r in RULES:
 if not db.query(Approval).filter_by(code=r['code']).first(): db.add(Approval(code=r['code'],name=r['name'],authority=r['authority'],sector=r['sector'],location='Maharashtra',min_size='Any',stages='New,Expansion,Operating',sla_days=r['sla_days'],sequence=r['sequence'],documents='|'.join(r['documents']),description='Configurable approval rule for the SIH26130 prototype.'))
if not db.query(Incentive).first(): db.add_all([Incentive(name='Maharashtra Industrial Incentive Support',sector='Manufacturing',state='Maharashtra',benefit='Potential capital / tax-linked support',eligibility='Sector, location and project-size dependent; verify current scheme terms.'),Incentive(name='Food Processing Support',sector='Food Processing',state='Maharashtra',benefit='Potential investment support',eligibility='Food processing projects meeting applicable scheme conditions.')])
u=db.query(User).filter_by(email='demo@civicme.in').first()
if u and not db.query(Renewal).filter_by(user_id=u.id).first(): db.add(Renewal(user_id=u.id,title='Factory Licence Renewal',due_date=datetime.utcnow()+timedelta(days=45)))
db.commit(); db.close(); print('Seed complete')
