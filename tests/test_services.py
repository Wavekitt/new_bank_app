import pytest
from src.services import investment_bank
import json


def test_empty_transactions():
    month = "2025-03"
    limit = 100
    result = investment_bank(month, [], limit)
    expected_result = '{\n    "Сумма, отложенная в «Инвесткопилку»": 0.0\n}'
    assert result == expected_result