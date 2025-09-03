NIL Platform

Structure
- nil-backend FastAPI app
- nil-frontend React app

Local with docker compose
- docker compose up --build
- Backend http://localhost:8000
- Frontend http://localhost:5173

Deployments
- Backend https://app-tezykswk.fly.dev
- Frontend https://nil-player-evaluation-app-a79n0hit.devinapps.com

Env
- Backend: DATABASE_URL, REDIS_URL
- Frontend: VITE_API_BASE_URL
