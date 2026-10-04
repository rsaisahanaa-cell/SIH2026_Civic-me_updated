# GitHub Pages deployment

1. Upload the contents of this project to the root of your GitHub repository (do not upload the ZIP as a ZIP).
2. Commit/push to the `main` branch.
3. Open **Settings → Pages** and set **Source = GitHub Actions**.
4. Open **Actions** and wait for **Deploy CIVIC@ME to GitHub Pages** to turn green.
5. Your site will be available at:
   https://rsaisahanaa-cell.github.io/SIH2026-CIVIC-ME/

## GitHub Pages demo mode
The Pages build uses `VITE_DEMO_MODE=true`, so the public demo does not depend on `localhost:8000`. It includes demo login, approval mapping, application tracking, document validation UI, SLA metrics, and official control-room flows using browser-local demo data.

Demo applicant: demo@civicme.in / Demo@123
Demo official: official@civicme.in / Officer@123

## Full-stack local mode
For the real FastAPI/PostgreSQL backend, use Docker Compose locally:

    docker compose up --build

Then open http://localhost:5173 and the frontend will use the backend at http://localhost:8000/api.
