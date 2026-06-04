"""HTML page routes (server-rendered Jinja2 templates).

Mounted at root path. Separate from REST API (api/v1/) to keep concerns split.
"""
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.BASE_DIR / "app" / "templates"))

_NO_CACHE = {"Cache-Control": "no-store, no-cache, must-revalidate", "Pragma": "no-cache"}


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, month: int = None, year: int = None):
    now = datetime.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"month": month, "year": year},
        headers=_NO_CACHE,
    )
