const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true';
const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const demoApprovals = [
  { code:'SPCB-CONSENT', authority:'Maharashtra Pollution Control Board', name:'Pollution Control Consent', sla_days:30, documents:['Site plan','Process flow','Land/lease proof'] },
  { code:'FACTORY-LIC', authority:'Factory Inspectorate', name:'Factory / Industrial Establishment Licence', sla_days:21, documents:['Building plan','Machinery list','Occupier details'] },
  { code:'FIRE-NOC', authority:'Fire & Emergency Services', name:'Fire Safety NOC', sla_days:15, documents:['Fire plan','Building layout','Safety equipment details'] },
  { code:'FSSAI', authority:'Food Safety Department', name:'Food Safety Registration / Licence', sla_days:15, documents:['Premises proof','Food category details','Identity proof'] }
];

const key = 'civicme-demo-state';
function state(){
  const saved = localStorage.getItem(key);
  if(saved) return JSON.parse(saved);
  const s = {
    profile: { name:'Demo Manufacturing Unit', sector:'Manufacturing', location:'Maharashtra', project_size:'Medium', stage:'New', employees:20 },
    applications: [], documents: {},
    users: {
      'demo@civicme.in': {id:1,name:'Demo Applicant',email:'demo@civicme.in',role:'applicant',password:'Demo@123'},
      'official@civicme.in': {id:2,name:'Demo Official',email:'official@civicme.in',role:'official',password:'Officer@123'}
    }
  };
  localStorage.setItem(key, JSON.stringify(s));
  return s;
}
function save(s){localStorage.setItem(key,JSON.stringify(s));return s}
function demoUser(){return JSON.parse(localStorage.getItem('user')||'null')}
function response(data){return Promise.resolve(data)}

function demoApi(path, opts={}){
  const s=state();
  const method=(opts.method||'GET').toUpperCase();
  const body=opts.body instanceof FormData ? null : (opts.body ? JSON.parse(opts.body) : {});
  const user=demoUser() || s.users['demo@civicme.in'];

  if(path==='/auth/login'){
    const u=s.users[body.email];
    if(!u || u.password!==body.password) return Promise.reject(new Error('Demo login failed. Use demo@civicme.in / Demo@123 or official@civicme.in / Officer@123'));
    return response({token:'demo-token',user:{id:u.id,name:u.name,email:u.email,role:u.role}});
  }
  if(path==='/auth/register'){
    const u={id:Date.now(),name:body.name,email:body.email,role:body.role||'applicant',password:body.password};
    s.users[u.email]=u; save(s); return response({token:'demo-token',user:{id:u.id,name:u.name,email:u.email,role:u.role}});
  }
  if(path==='/dashboard'){
    const apps=s.applications;
    return response({role:user.role,profile:!!s.profile,metrics:{applications:apps.length,in_review:apps.filter(a=>['Submitted','Under Review'].includes(a.status)).length,approved:apps.filter(a=>a.status==='Approved').length,documents:Object.values(s.documents).flat().length,sla_at_risk:apps.filter(a=>a.status!=='Approved').length>0?1:0},renewals:[{id:1,title:'Factory Licence Renewal',due_date:'2026-12-15'}],incentives:[{id:1,name:'Maharashtra Industrial Incentive Scheme',description:'Explore applicable state support and incentives.'}]});
  }
  if(path==='/profile'){
    if(method==='POST'){s.profile=body;save(s);return response(s.profile)}
    return response(s.profile);
  }
  if(path==='/approvals/map') return response({profile_required:!s.profile,profile:s.profile,approvals:demoApprovals});
  if(path==='/applications' && method==='GET') return response(s.applications);
  if(path==='/applications' && method==='POST'){
    const a=demoApprovals.find(x=>x.code===body.approval_code);
    const id=Date.now(); const now=new Date(); const due=new Date(now); due.setDate(due.getDate()+(a?.sla_days||15));
    const app={id,reference:'CIVIC-'+String(id).slice(-6),approval_id:id,status:'Draft',submitted_at:null,due_at:due.toISOString(),department:a?.authority||'Department',query:null,steps:['Application Intake','Document Scrutiny','Inspection / Query','Decision'].map((step,i)=>({step_name:step,status:'Pending',sequence:i+1}))};
    s.applications.unshift(app);s.documents[id]=[];save(s);return response(app);
  }
  const sub=path.match(/^\/applications\/(\d+)\/(submit|advance)$/);
  if(sub){
    const app=s.applications.find(a=>a.id===Number(sub[1]));
    if(!app) return Promise.reject(new Error('Application not found'));
    if(sub[2]==='submit'){app.status='Submitted';app.submitted_at=new Date().toISOString();app.steps[0].status='In Review';}
    else {const cur=app.steps.find(x=>x.status==='In Review');if(cur){cur.status='Completed';const next=app.steps.find(x=>x.status==='Pending');if(next){next.status='In Review';app.status='Under Review'}else app.status='Approved'} }
    save(s);return response(app);
  }
  const doc=path.match(/^\/documents\/(\d+)(?:\/upload)?$/);
  if(doc){
    const id=Number(doc[1]);
    if(method==='GET') return response(s.documents[id]||[]);
    if(method==='POST'){
      const file=opts.body?.get('file');
      if(!file) return Promise.reject(new Error('Choose a document first'));
      const d={id:Date.now(),original_name:file.name,size_bytes:file.size,validation_score:file.size>500?100:75,validation_notes:'Demo mode: format and file-size pre-check passed.'};
      s.documents[id]=[...(s.documents[id]||[]),d];save(s);return response(d);
    }
  }
  if(path==='/official/dashboard'){
    const apps=s.applications;return response({total:apps.length,submitted:apps.filter(a=>a.status==='Submitted').length,under_review:apps.filter(a=>a.status==='Under Review').length,approved:apps.filter(a=>a.status==='Approved').length,sla_at_risk:apps.filter(a=>a.status!=='Approved').length>0?1:0,applications:apps.map(a=>({id:a.id,reference:a.reference,status:a.status,department:a.department,due_at:a.due_at,user_id:1}))});
  }
  const off=path.match(/^\/official\/applications\/(\d+)\/advance$/);
  if(off){
    const app=s.applications.find(a=>a.id===Number(off[1])); if(!app)return Promise.reject(new Error('Application not found'));
    const cur=app.steps.find(x=>x.status==='In Review'); if(cur){cur.status='Completed';const next=app.steps.find(x=>x.status==='Pending');if(next){next.status='In Review';app.status='Under Review'}else app.status='Approved'} save(s);return response({status:app.status});
  }
  return response({});
}

export async function api(path,opts={}){
  if(DEMO_MODE) return demoApi(path,opts);
  const h=new Headers(opts.headers||{});const t=localStorage.getItem('token');if(t)h.set('Authorization',`Bearer ${t}`);if(!(opts.body instanceof FormData))h.set('Content-Type','application/json');
  const r=await fetch(BASE+path,{...opts,headers:h});const data=await r.json().catch(()=>({}));if(!r.ok)throw new Error(data.detail||'Request failed');return data;
}
export const login=(x)=>api('/auth/login',{method:'POST',body:JSON.stringify(x)});
export const register=(x)=>api('/auth/register',{method:'POST',body:JSON.stringify(x)});
