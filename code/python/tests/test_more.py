import builtins
import importlib
import main
import operations
import data
from data import read_balance, write_balance


def make_input_sequence(seq):
    it = iter(seq)
    return lambda prompt='': next(it)


def test_menu_routes_to_actions_and_exit(monkeypatch, capsys):
    # TC-01: supply choice 1 (view balance) then 4 (exit)
    monkeypatch.setattr('builtins.input', make_input_sequence(['1', '4']))
    main.main()
    out = capsys.readouterr().out
    assert "Current balance:" in out
    assert "Exiting the program. Goodbye!" in out


def test_invalid_menu_choice_shows_message(monkeypatch, capsys):
    # TC-14: supply invalid choice then exit
    monkeypatch.setattr('builtins.input', make_input_sequence(['5', '4']))
    main.main()
    out = capsys.readouterr().out
    assert "Invalid choice, please select 1-4." in out


def test_multiple_sequential_operations_persist():
    # TC-07: credit 100, debit 50 -> final 1050
    write_balance(1000.00)
    # perform credit
    monkeypatch_input = lambda prompt='': '100.00'
    builtins_input = builtins.input
    try:
        builtins.input = monkeypatch_input
        operations.perform_operation('CREDIT')
        builtins.input = lambda prompt='': '50.00'
        operations.perform_operation('DEBIT')
    finally:
        builtins.input = builtins_input

    assert abs(read_balance() - 1050.00) < 1e-6


def test_overflow_amount_is_handled(monkeypatch):
    # TC-13: enter a very large credit and observe Python port behavior
    write_balance(1000.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': '1000000.00')
    operations.perform_operation('CREDIT')
    # Python port accepts large values; balance increases accordingly
    assert abs(read_balance() - 1001000.00) < 1e-6


def test_exit_option_terminates_cleanly(monkeypatch, capsys):
    # TC-15: supply exit directly
    monkeypatch.setattr('builtins.input', make_input_sequence(['4']))
    main.main()
    out = capsys.readouterr().out
    assert "Exiting the program. Goodbye!" in out


def test_persistence_across_module_reload():
    # TC-16: write balance, reload module, storage should reset to initial 1000.00
    write_balance(1200.00)
    importlib.reload(data)
    assert abs(data.read_balance() - 1000.00) < 1e-6


def test_read_then_write_no_change(monkeypatch, capsys):
    # TC-17: read then credit 0.00 then read -> no change
    write_balance(1000.00)
    # view
    operations.perform_operation('TOTAL')
    # credit 0.00
    monkeypatch.setattr('builtins.input', lambda prompt='': '0.00')
    operations.perform_operation('CREDIT')
    # view again
    operations.perform_operation('TOTAL')
    out = capsys.readouterr().out
    # last reported balance should be 1000.00
    assert out.strip().endswith('Current balance: 1000.00')


def test_input_precision_shows_two_decimals(monkeypatch, capsys):
    # TC-18: enter 0.1 and expect displayed 1000.10
    write_balance(1000.00)
    monkeypatch.setattr('builtins.input', lambda prompt='': '0.1')
    operations.perform_operation('CREDIT')
    out = capsys.readouterr().out
    assert "New balance: 1000.10" in out
