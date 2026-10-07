"""Project Vishnu — Configuration

Central configuration for the Vishnu backend server.
"""
import os
from pathlib import Path


# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "vishnu.db"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# ── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# ── Server ───────────────────────────────────────────────────────────────────
API_PREFIX = "/api"
PROJECT_NAME = "Vishnu — openGotham"
PROJECT_DESCRIPTION = (
    "Open-source intelligence integration, operational analysis, "
    "and defense analytics platform — an alternative to Palantir Gotham."
)
VERSION = "0.1.0"

# ── CORS ─────────────────────────────────────────────────────────────────────
CORS_ORIGINS: list[str] = [
    "http://localhost:5173",   # Vite dev server
    "http://localhost:3000",   # Alternative React port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# ── Classification Levels ────────────────────────────────────────────────────
CLASSIFICATION_LEVELS = [
    "UNCLASSIFIED",
    "RESTRICTED",
    "CONFIDENTIAL",
    "SECRET",
    "TOP_SECRET",
]

# ── Entity Types ─────────────────────────────────────────────────────────────
ENTITY_TYPES = [
    "person",
    "organization",
    "location",
    "vehicle",
    "event",
    "document",
]

# ── Relationship Types ───────────────────────────────────────────────────────
RELATIONSHIP_TYPES = [
    "ASSOCIATED_WITH",
    "WORKS_FOR",
    "LOCATED_AT",
    "OWNS",
    "COMMUNICATED_WITH",
    "TRAVELED_TO",
    "PARTICIPATED_IN",
    "FUNDED_BY",
    "MEMBER_OF",
    "RELATED_TO",
    "COMMANDS",
    "REPORTS_TO",
    "SUPPLIER_OF",
    "SIBLING_OF",
    "KNOWN_ALIAS",
]
