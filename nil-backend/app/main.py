from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routers import health as health_router
from .api.routers import players, optimize, compliance, ingest, analytics
from .data.seed import load_seed

app = FastAPI(title="NIL Moneyball API")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router, tags=["Health"])
app.include_router(players.router, prefix="/api/v1", tags=["Players"])
app.include_router(optimize.router, prefix="/api/v1", tags=["Optimization"])
app.include_router(compliance.router, prefix="/api/v1", tags=["Compliance"])
app.include_router(ingest.router, prefix="/api/v1", tags=["Ingest"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])


@app.on_event("startup")
def startup():
    load_seed()
