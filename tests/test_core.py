"""Tests for budget.core."""

from budget.core import add_transaction


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the list length by one."""
    transactions = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0] == transaction


def test_add_transaction_preserves_negative_amount_expense() -> None:
    """Expense transactions with negative amounts should be stored as-is."""
    transactions = []
    transaction = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0]["amount"] == -12000
    assert result[0]["type"] == "지출"


def test_add_transaction_preserves_positive_amount_income() -> None:
    """Income transactions with positive amounts should be stored as-is."""
    transactions = []
    transaction = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "중고 판매",
        "amount": 25000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0] == transaction


def test_add_transaction_allows_empty_description() -> None:
    """Empty descriptions should be accepted and stored unchanged."""
    transactions = []
    transaction = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0]["description"] == ""
