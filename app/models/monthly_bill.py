from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class MonthlyBill(Base):
    __tablename__ = "monthly_bills"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    month = Column(Integer)
    year = Column(Integer)
    electricity_fee = Column(Integer)
    rent_fee = Column(Integer)
    service_fee = Column(Integer)
    total = Column(Integer)
    status = Column(String)  # "unpaid", "paid", "prepaid"
    prepaid_months = Column(String, nullable=True)
    paid_at = Column(DateTime, nullable=True)

    tenant_name = Column(String, nullable=True)
    move_in_date = Column(String, nullable=True)

    room = relationship("Room", back_populates="bills")

    # Quy tắc nghiệp vụ "thế nào là đã thu / còn nợ" được đóng gói trong chính
    # đối tượng, thay vì rải `status == "..."` khắp endpoint và service.
    PAID_STATUSES = ("paid", "prepaid")

    @property
    def is_paid(self) -> bool:
        """Đã thu (thanh toán trực tiếp hoặc đóng trước)."""
        return self.status in self.PAID_STATUSES

    @property
    def is_overdue(self) -> bool:
        """Còn nợ — hoá đơn chưa được thu."""
        return not self.is_paid
