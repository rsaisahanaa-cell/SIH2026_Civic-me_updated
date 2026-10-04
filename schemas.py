from datetime import date
from pydantic import BaseModel, ConfigDict

class ProfileCreate(BaseModel):
    name: str
    sector: str
    location: str
    project_size: str
    operating_stage: str
    owner_name: str = "Demo Applicant"

class ProfileOut(ProfileCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ApprovalOut(BaseModel):
    id: int
    code: str
    name: str
    department: str
    description: str
    sla_days: int
    sequence: int
    model_config = ConfigDict(from_attributes=True)

class ApplicationCreate(BaseModel):
    profile_id: int
    approval_id: int

class ApplicationOut(BaseModel):
    id: int
    reference_no: str
    approval_name: str
    department: str
    status: str
    submitted_at: str
    due_date: date
    sla_state: str

class DocumentCheck(BaseModel):
    requirement_id: int
    filename: str

class DocumentOut(BaseModel):
    id: int
    requirement_id: int
    filename: str
    status: str
    validation_message: str
    model_config = ConfigDict(from_attributes=True)

class WorkflowOut(BaseModel):
    id: int
    department: str
    step_name: str
    status: str
    due_date: date
    model_config = ConfigDict(from_attributes=True)

class DashboardOut(BaseModel):
    total_applications: int
    pending: int
    approved: int
    overdue: int
    documents_pending: int
    renewals_due: int
