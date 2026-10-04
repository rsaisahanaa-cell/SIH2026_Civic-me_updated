from datetime import date, timedelta, datetime
from pathlib import Path
from .rules import applicable_rules

ALLOWED_EXTS = {".pdf", ".png", ".jpg", ".jpeg"}

def sla_state(due_date):
    if due_date < date.today():
        return "overdue"
    days = (due_date - date.today()).days
    if days <= 3:
        return "due_soon"
    return "on_track"

def validate_document(filename: str, requirement_name: str):
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTS:
        return "rejected", f"Unsupported file type {ext or '(none)'}. Use PDF/PNG/JPG."
    if Path(filename).name.strip() == "":
        return "rejected", "Filename is required."
    # Prototype validation: real OCR/content validation should be added later.
    return "validated", f"Filename/type check passed for requirement: {requirement_name}."

def make_reference(app_id):
    return f"CIVIC-{datetime.utcnow().year}-{app_id:05d}"
