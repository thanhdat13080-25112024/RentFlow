"""Strategy pattern cho cách tính tiền điện.

Mỗi loại điện (`Room.electricity_type`) là một lớp chiến lược riêng kế thừa lớp
trừu tượng `ElectricityStrategy`. Nhờ vậy việc chọn công thức tính tiền là **đa
hình subtype** thật sự — thay cho khối `if/elif` rải trong tầng service.

Thêm một loại điện mới = thêm một lớp + đăng ký vào `_STRATEGIES`, không phải sửa
hàm tính tiền.

Module này KHÔNG import model ở mức thực thi (chỉ type-hint khi kiểm tra kiểu) nên
không tạo vòng import với `app.services.billing`.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # tránh import vòng; chỉ dùng cho gợi ý kiểu khi type-check
    from app.models import ElectricityReading, Room


class ElectricityStrategy(ABC):
    """Giao diện chung: nhận một phòng + chỉ số điện (có thể None) → trả tiền điện."""

    @abstractmethod
    def fee(self, room: "Room", reading: Optional["ElectricityReading"]) -> int:
        ...


class MeterStrategy(ElectricityStrategy):
    """Tính theo số điện tiêu thụ: (mới − cũ) × đơn giá. Không có chỉ số → 0."""

    def fee(self, room: "Room", reading: Optional["ElectricityReading"]) -> int:
        if not reading:
            return 0
        return (reading.new_reading - reading.old_reading) * reading.unit_price


class FixedStrategy(ElectricityStrategy):
    """Khoán: dùng phí cố định của phòng, bỏ qua chỉ số đồng hồ."""

    def fee(self, room: "Room", reading: Optional["ElectricityReading"]) -> int:
        return room.fixed_electricity_fee or 0


# Bảng tra: electricity_type -> instance chiến lược (tái dùng, không trạng thái).
_STRATEGIES: dict[str, ElectricityStrategy] = {
    "meter": MeterStrategy(),
    "fixed": FixedStrategy(),
}

# Phòng thiếu/không rõ loại điện thì coi như tính theo đồng hồ.
_DEFAULT_STRATEGY: ElectricityStrategy = _STRATEGIES["meter"]


def strategy_for(room: "Room") -> ElectricityStrategy:
    """Chọn chiến lược theo `room.electricity_type` (mặc định: meter)."""
    return _STRATEGIES.get(room.electricity_type, _DEFAULT_STRATEGY)


def electricity_fee(room: "Room", reading: Optional["ElectricityReading"]) -> int:
    """Điểm vào tiện lợi: chọn chiến lược rồi tính — không if/elif ở nơi gọi."""
    return strategy_for(room).fee(room, reading)
