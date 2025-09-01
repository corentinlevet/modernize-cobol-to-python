"""Simple in-memory storage converted from `data.cob`.
Provides read_balance() and write_balance().
"""

_STORAGE_BALANCE = 1000.00


def read_balance() -> float:
    """Return the stored balance."""
    return _STORAGE_BALANCE


def write_balance(balance: float) -> None:
    """Update the stored balance (in-memory)."""
    global _STORAGE_BALANCE
    _STORAGE_BALANCE = float(balance)
