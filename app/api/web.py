"""HTML page routes (server-rendered Jinja2 templates).

Mounted at root path. Separate from REST API (api/v1/) to keep concerns split.
"""
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt

from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, month: int = None, year: int = None):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")

    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        return RedirectResponse(url="/login")

    now = datetime.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year
    return templates.TemplateResponse(
        request=request, name="index.html", context={"month": month, "year": year}
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")
