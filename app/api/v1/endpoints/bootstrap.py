from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Room, Setting
from app.schemas import BootstrapRead
from app.api.v1.endpoints.bills import _collect_bills, _get_revenue_summary, _get_receivables

router = APIRouter()

@router.get("/", response_model=BootstrapRead)
async def bootstrap(month: int, year: int, db: Session = Depends(get_db)):
    """Gộp các request khởi tạo dashboard vào 1 lần gọi để giảm cold-start overhead."""
    # 1. Bills cho tháng hiện tại
    bills = _collect_bills(db, month, year)
    
    # 2. Settings
    settings_data = db.query(Setting).all()
    settings = {s.key: s.value for s in settings_data}
    
    # 3. Rooms
    rooms = db.query(Room).all()
    
    # 4. Revenue Summary
    revenue_summary = _get_revenue_summary(db)
    
    # 5. Receivables
    receivables = _get_receivables(db)
    
    return {
        "bills": bills,
        "settings": settings,
        "rooms": rooms,
        "revenue_summary": revenue_summary,
        "receivables": receivables
    }
