from typing import Any, Dict, List

from pydantic import BaseModel

from app.schemas.bill import BillRead, RevenueSummaryRead
from app.schemas.room import RoomRead

class BootstrapRead(BaseModel):
    bills: List[Dict[str, Any]]  # _collect_bills returns dicts
    settings: Dict[str, str]
    rooms: List[RoomRead]
    revenue_summary: List[RevenueSummaryRead]
    receivables: Dict[str, Any]
