"""FastAPI dependency injection helpers.

Single import point for routers needing common deps (DB session, auth).
"""
from app.core.security import get_current_user
from app.db import get_db

__all__ = ["get_db", "get_current_user"]
