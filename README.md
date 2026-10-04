# CIVIC@ME — SIH26130 Competition-Ready Prototype

An intelligent industrial approval and compliance accelerator aligned to SIH26130. It demonstrates a unified journey: Business Profile → Approval Discovery → Document Validation → Workflow → SLA Tracking → Renewals & Incentives.

## What is included
- Applicant and Government Official roles with JWT login.
- Business profile and rule-driven Approval Mapper.
- Sector-aware approval discovery with authority, SLA and document requirements.
- Real multipart document upload to persistent Docker storage (10 MB limit, supported formats).
- Document pre-validation score and status.
- Application lifecycle: Draft → Submitted → Under Review → Approved.
- Workflow steps: intake, scrutiny, inspection/query, decision.
- SLA due dates and at-risk metric.
- Applicant command centre and Government Official control room.
- Seeded demo users, approval rules, incentive and renewal data.
- PostgreSQL persistence through Docker Compose.
- API docs at http://localhost:8000/docs.

## Run locally
Prerequisite: Docker Desktop.

```bash
docker compose up --build
```

Open http://localhost:5173.

### Demo credentials
Applicant: `demo@civicme.in` / `Demo@123`

Official: `official@civicme.in` / `Officer@123`

## Important prototype note
This is a competition/demo implementation, not a production government portal. Approval rules and scheme data are illustrative and must be verified against current official regulations before real-world use. The document validator demonstrates format/size pre-checking; production deployment should add OCR, malware scanning, encryption/key management, immutable audit logs, official API adapters, current regulatory data governance and human review.

## Project mapping to SIH26130
**Problem:** fragmented registrations, licences, NOCs, inspections, renewals and support schemes.

**Solution:** one intelligent layer that discovers applicable approvals, guides documents, coordinates workflow and exposes SLA/renewal/incentive visibility.

**MVP flow:** Profile → Rules Engine → Approval Checklist → Document Upload/Pre-check → Submit → Parallel-ready Workflow → SLA Monitoring → Inspection/Query → Decision → Renewal & Incentives.

## GitHub Pages

The repository includes `.github/workflows/deploy.yml` and a GitHub Pages demo build. Set **Settings → Pages → Source → GitHub Actions**. The workflow builds the React frontend with the repository base path `/SIH2026-CIVIC-ME/` and enables demo mode so the public site does not call `localhost:8000`.

See `GITHUB-PAGES-SETUP.md` for the exact steps.
