"""HTML page routes (server-rendered Jinja2 templates).

Mounted at root path. Separate from REST API (api/v1/) to keep concerns split.
"""
from datetime import datetime
import json
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.endpoints.bills import _collect_bills, _get_revenue_summary, _get_receivables
from app.models import Room, Setting
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.BASE_DIR / "app" / "templates"))

_NO_CACHE = {"Cache-Control": "no-store, no-cache, must-revalidate", "Pragma": "no-cache"}


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, month: int = None, year: int = None, db: Session = Depends(get_db)):
    now = datetime.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year

    # Hydrate data: fetch bootstrap data server-side to avoid extra client-side request
    bills = _collect_bills(db, month, year)
    settings_data = db.query(Setting).all()
    rooms_data = db.query(Room).all()
    # Manual conversion to dict for Room models to be JSON serializable
    rooms = [
        {
            "id": r.id, "room_number": r.room_number, "rent_price": r.rent_price,
            "service_fee": r.service_fee, "deposit": r.deposit,
            "contact_info": r.contact_info, "move_in_date": r.move_in_date,
            "is_occupied": r.is_occupied, "electricity_type": r.electricity_type,
            "fixed_electricity_fee": r.fixed_electricity_fee
        }
        for r in rooms_data
    ]
    revenue_summary = _get_revenue_summary(db)
    receivables = _get_receivables(db)

    bootstrap_data = {
        "bills": bills,
        "settings": {s.key: s.value for s in settings_data},
        "rooms": rooms,
        "revenue_summary": revenue_summary,
        "receivables": receivables
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "month": month,
            "year": year,
            "bootstrap_data": json.dumps(bootstrap_data)
        },
        headers=_NO_CACHE,
    )
