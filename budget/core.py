"""Core domain functions for the budget CLI app."""

from __future__ import annotations

import csv
from pathlib import Path
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


def get_balance(transactions: list[dict[str, Any]]) -> float:
    """Return the sum of signed transaction amounts."""
    if not transactions:
        return 0.0
    return float(sum(transaction["amount"] for transaction in transactions))


def filter_by_category(transactions: list[dict[str, Any]], category: str) -> list[dict[str, Any]]:
    """Return transactions that match the given category, ignoring case."""
    normalized_category = category.casefold()
    return [
        transaction
        for transaction in transactions
        if transaction["category"].casefold() == normalized_category
    ]


def load_transactions_from_csv(csv_path: str | Path) -> list[dict[str, Any]]:
    """Load transactions from a CSV file and normalize the amount field."""
    path = Path(csv_path)
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            {
                "date": row["date"],
                "type": row["type"],
                "category": row["category"],
                "description": row["description"],
                "amount": int(row["amount"]),
                "memo": row["memo"],
            }
            for row in reader
        ]
