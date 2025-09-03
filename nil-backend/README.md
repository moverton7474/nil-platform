NIL Moneyball Backend (FastAPI)

Run locally
- poetry install
- poetry run fastapi dev app/main.py
- Open http://127.0.0.1:8000/docs

Key endpoints
- GET /healthz
- GET /api/v1/players?position=LB
- GET /api/v1/players/{athlete_id}
- GET /api/v1/players/{athlete_id}/baron
- POST /api/v1/optimize/roster
- POST /api/v1/offers/validate
- POST /api/v1/offers/simulate-compliance
- POST /api/v1/ingest/players
- GET /api/v1/analytics/value-finds

Notes
- In-memory data and cache; Redis/Postgres planned post-MVP.
- Budget tiers: Group5_Low $800K; Group5_High $1.3M; Power4_Standard $8.5M; Power4_Elite $20.5M.
- Baron Hopson baseline baked into evaluator and seed.
