"""Operations module converted from `operations.cob`.
Handles: TOTAL, CREDIT, DEBIT using `data` as storage.
"""
from data import read_balance, write_balance


def perform_operation(op_type: str) -> None:
    op = op_type.strip().upper()

    if op == 'TOTAL':
        bal = read_balance()
        print(f"Current balance: {bal:.2f}")

    elif op == 'CREDIT':
        try:
            amount_str = input("Enter credit amount: ").strip()
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount entered.")
            return

        bal = read_balance()
        bal += amount
        write_balance(bal)
        print(f"Amount credited. New balance: {bal:.2f}")

    elif op == 'DEBIT':
        try:
            amount_str = input("Enter debit amount: ").strip()
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount entered.")
            return

        bal = read_balance()
        if bal >= amount:
            bal -= amount
            write_balance(bal)
            print(f"Amount debited. New balance: {bal:.2f}")
        else:
            print("Insufficient funds for this debit.")

    else:
        print("Unknown operation.")
