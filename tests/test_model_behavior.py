"""Unit tests for behaviour added to the domain models.

These properties move the "what counts as paid / overdue" rule *into* the model
(encapsulation) instead of scattering `status == "..."` string checks across the
codebase.
"""
from app.models import MonthlyBill


def test_is_paid_true_for_paid():
    assert MonthlyBill(status="paid").is_paid is True


def test_is_paid_true_for_prepaid():
    assert MonthlyBill(status="prepaid").is_paid is True


def test_is_paid_false_for_unpaid():
    assert MonthlyBill(status="unpaid").is_paid is False


def test_is_overdue_true_only_for_unpaid():
    assert MonthlyBill(status="unpaid").is_overdue is True
    assert MonthlyBill(status="paid").is_overdue is False
    assert MonthlyBill(status="prepaid").is_overdue is False


def test_is_paid_and_is_overdue_are_opposite():
    for status in ("unpaid", "paid", "prepaid"):
        bill = MonthlyBill(status=status)
        assert bill.is_paid is not bill.is_overdue
