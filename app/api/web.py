"""HTML page routes (server-rendered Jinja2 templates).

Mounted at root path. Separate from REST API (api/v1/) to keep concerns split.
"""
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.security import get_subject_from_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_NO_CACHE = {"Cache-Control": "no-store, no-cache, must-revalidate", "Pragma": "no-cache"}


def _current_user(request: Request) -> str | None:
    """Username từ cookie nếu đã đăng nhập hợp lệ, ngược lại None."""
    return get_subject_from_token(request.cookies.get("access_token"))


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # Đã đăng nhập rồi thì khỏi xem trang login nữa.
    if _current_user(request):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request=request, name="login.html", headers=_NO_CACHE)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, month: int = None, year: int = None):
    # Chưa đăng nhập → đẩy về trang login (trang chính chứa dữ liệu khách thuê).
    if not _current_user(request):
        return RedirectResponse(url="/login", status_code=302)

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
