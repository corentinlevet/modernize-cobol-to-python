import builtins
import operations
from data import read_balance, write_balance


def test_view_balance(capsys):
    write_balance(1000.00)
    operations.perform_operation('TOTAL')
    out = capsys.readouterr().out
    assert "Current balance: 1000.00" in out


def test_credit_valid(monkeypatch, capsys):
    write_balance(1000.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': '200.50')
    operations.perform_operation('CREDIT')
    out = capsys.readouterr().out
    assert "Amount credited. New balance: 1200.50" in out
    assert abs(read_balance() - 1200.50) < 1e-6


def test_debit_valid(monkeypatch, capsys):
    write_balance(1000.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': '250.25')
    operations.perform_operation('DEBIT')
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 749.75" in out
    assert abs(read_balance() - 749.75) < 1e-6


def test_debit_equal(monkeypatch, capsys):
    write_balance(500.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': '500.00')
    operations.perform_operation('DEBIT')
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 0.00" in out
    assert abs(read_balance() - 0.00) < 1e-6


def test_debit_insufficient(monkeypatch, capsys):
    write_balance(300.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': '400.00')
    operations.perform_operation('DEBIT')
    out = capsys.readouterr().out
    assert "Insufficient funds for this debit." in out
    assert abs(read_balance() - 300.00) < 1e-6


def test_zero_credit_and_debit(monkeypatch, capsys):
    write_balance(1000.00)
    # credit zero
    monkeypatch.setattr('builtins.input', lambda prompt='': '0.00')
    operations.perform_operation('CREDIT')
    out = capsys.readouterr().out
    assert "Amount credited. New balance: 1000.00" in out
    assert abs(read_balance() - 1000.00) < 1e-6

    # debit zero
    monkeypatch.setattr('builtins.input', lambda prompt='': '0.00')
    operations.perform_operation('DEBIT')
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 1000.00" in out
    assert abs(read_balance() - 1000.00) < 1e-6


def test_negative_credit_and_debit(monkeypatch, capsys):
    write_balance(1000.00)
    # negative credit -> reduces balance (current behavior)
    monkeypatch.setattr('builtins.input', lambda prompt='': '-100.00')
    operations.perform_operation('CREDIT')
    out = capsys.readouterr().out
    assert "Amount credited. New balance: 900.00" in out
    assert abs(read_balance() - 900.00) < 1e-6

    # negative debit -> increases balance (current behavior)
    monkeypatch.setattr('builtins.input', lambda prompt='': '-50.00')
    operations.perform_operation('DEBIT')
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 950.00" in out
    assert abs(read_balance() - 950.00) < 1e-6


def test_non_numeric_input(monkeypatch, capsys):
    write_balance(1000.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': 'abc')
    operations.perform_operation('CREDIT')
    out = capsys.readouterr().out
    assert "Invalid amount entered." in out
    assert abs(read_balance() - 1000.00) < 1e-6
