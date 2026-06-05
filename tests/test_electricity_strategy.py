"""Unit tests for the electricity-fee Strategy pattern
(app/services/electricity_strategy.py).

These lock in the polymorphic behaviour: each electricity type is a separate
strategy class, and `electricity_fee()` dispatches to the right one without any
`if/elif` at the call site.
"""
from app.models import ElectricityReading, Room
from app.services.electricity_strategy import (
    ElectricityStrategy,
    FixedStrategy,
    MeterStrategy,
    electricity_fee,
    strategy_for,
)


def _room(**kw):
    defaults = dict(
        room_number="101", rent_price=2000000, service_fee=100000,
        electricity_type="meter", fixed_electricity_fee=0, is_occupied=True,
    )
    defaults.update(kw)
    return Room(**defaults)


# ── MeterStrategy: usage × unit price ──

def test_meter_strategy_with_reading():
    s = MeterStrategy()
    reading = ElectricityReading(old_reading=100, new_reading=150, unit_price=4000)
    assert s.fee(_room(electricity_type="meter"), reading) == 200000  # (150-100)*4000


def test_meter_strategy_without_reading_is_zero():
    assert MeterStrategy().fee(_room(electricity_type="meter"), None) == 0


# ── FixedStrategy: flat fee, ignores the meter reading ──

def test_fixed_strategy_uses_flat_fee():
    room = _room(electricity_type="fixed", fixed_electricity_fee=150000)
    reading = ElectricityReading(old_reading=0, new_reading=9999, unit_price=4000)
    assert FixedStrategy().fee(room, reading) == 150000


def test_fixed_strategy_none_fee_is_zero():
    room = _room(electricity_type="fixed", fixed_electricity_fee=None)
    assert FixedStrategy().fee(room, None) == 0


# ── Polymorphic dispatch: no if/elif at the call site ──

def test_strategy_for_returns_subtype():
    assert isinstance(strategy_for(_room(electricity_type="meter")), MeterStrategy)
    assert isinstance(strategy_for(_room(electricity_type="fixed")), FixedStrategy)
    # Every strategy is an ElectricityStrategy (shared abstract base).
    assert isinstance(strategy_for(_room()), ElectricityStrategy)


def test_electricity_fee_dispatches_by_type():
    meter = _room(electricity_type="meter")
    reading = ElectricityReading(old_reading=10, new_reading=60, unit_price=3500)
    assert electricity_fee(meter, reading) == 175000          # (60-10)*3500

    fixed = _room(electricity_type="fixed", fixed_electricity_fee=200000)
    assert electricity_fee(fixed, reading) == 200000          # reading ignored
