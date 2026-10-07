"""Project Vishnu — FastAPI Application

Main entry point that wires up all routers, middleware, and database init.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_PREFIX, CORS_ORIGINS, PROJECT_DESCRIPTION, PROJECT_NAME, VERSION
from app.database import init_db
from app.routers import entities, graph, ingest, relationships, search


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle hook."""
    # Create tables on first run
    init_db()
    yield


app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(entities.router, prefix=API_PREFIX)
app.include_router(relationships.router, prefix=API_PREFIX)
app.include_router(graph.router, prefix=API_PREFIX)
app.include_router(search.router, prefix=API_PREFIX)
app.include_router(ingest.router, prefix=API_PREFIX)


# ── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root() -> dict:
    """Health check / welcome endpoint."""
    return {
        "project": PROJECT_NAME,
        "version": VERSION,
        "status": "operational",
        "docs": "/docs",
        "message": "🔱 Vishnu (openGotham) is running. Visit /docs for the API explorer.",
    }
