import pytest
from src.views import get_date_range, main_func
from src.utils import analyze_cards, read_xlsx, get_greeting
import json


def test_get_date_range():
    # Проверяем с правильной датой
    input_date = "15.03.2025"
    expected_output = "01.03.2025 - 15.03.2025"
    assert get_date_range(input_date) == expected_output

    # Проверяем с другой датой
    input_date = "01.01.2025"
    expected_output = "01.01.2025 - 01.01.2025"
    assert get_date_range(input_date) == expected_output


def test_main_func(mock_read_xlsx, mock_get_greeting, mock_analyze_cards):
    expected_result = {
        "greeting": "Здравствуйте",
        "cards": ["card_1", "card_2"]
    }

    result = main_func()
    assert json.loads(result) == expected_result