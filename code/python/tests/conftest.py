import sys
import os
import pytest

# Ensure src is importable when running tests from repository root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from data import write_balance

@pytest.fixture(autouse=True)
def reset_balance():
    # reset before each test
    write_balance(1000.00)
    yield
    write_balance(1000.00)
