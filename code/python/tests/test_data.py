from data import read_balance, write_balance


def test_read_write():
    write_balance(1500.25)
    assert read_balance() == 1500.25
