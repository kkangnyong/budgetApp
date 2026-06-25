"""Core domain functions for the budget CLI app."""

from __future__ import annotations

from typing import Any


def add_transaction(transactions: list[dict[str, Any]], transaction: dict[str, Any]) -> list[dict[str, Any]]:
    """Add a transaction to the transaction list and return the updated list."""
    normalized_transaction: dict[str, Any] = {
        "date": transaction["date"],
        "type": transaction["type"],
        "category": transaction["category"],
        "description": transaction.get("description", ""),
        "amount": transaction["amount"],
        "memo": transaction.get("memo", ""),
    }
    transactions.append(normalized_transaction)
    return transactions
