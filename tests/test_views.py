import json
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest
import pandas as pd
from pathlib import Path
from src.views import get_date_range, main_func


@pytest.mark.parametrize("input_date, expected_start, expected_end", [
    ("2025-03-15 00:00:00", datetime(2025, 3, 1, 0, 0), datetime(2025, 3, 15, 0, 0)),
    ("2025-01-01 12:30:45", datetime(2025, 1, 1, 12, 30, 45), datetime(2025, 1, 1, 12, 30, 45)),
])
def test_get_date_range(input_date, expected_start, expected_end):
    """Тест проверяет, что функция возвращает корректные datetime объекты с сохранением времени"""
    start, end = get_date_range(input_date)
    assert start == expected_start, "Некорректная начальная дата"
    assert end == expected_end, "Некорректная конечная дата"


@patch('pandas.read_excel')
@patch('src.views.get_greeting', return_value="Добрый день")
@patch('src.views.analyze_cards', return_value=[{"card_number": "1234", "total_expenses": 1000}])
@patch('src.views.get_top_five_trans', return_value=[])
@patch('src.views.convertation_currency', return_value={"USD": 75, "EUR": 85})
@patch('src.views.get_stocks_prices', return_value={"AAPL": 150, "TSLA": 700})
def test_main_func(mock_get_stocks_prices, mock_convertation_currency, mock_top_five,
                   mock_analyze_cards, mock_greeting, mock_read_excel):
    input_date = "2023-10-15 12:00:00"
    test_data = pd.DataFrame({
        'Дата операции': [
            pd.Timestamp('2023-10-01'),
            pd.Timestamp('2023-10-15 12:00:00'),
            pd.Timestamp('2023-10-31')
        ],
        'Другие колонки': [1, 2, 3]
    })
    mock_read_excel.return_value = test_data
    result = main_func(input_date)
    result_data = json.loads(result)
    assert mock_read_excel.call_args[0][0].name == 'operations.xlsx'
    assert "greeting" in result_data
    assert "Отчёт за период:" in result_data["greeting"]  # Проверяем часть строки
    assert "01.10.2023 - 15.10.2023" in result_data["greeting"]
    assert "cards" in result_data
    assert len(result_data["cards"]) == 1
    assert result_data["cards"][0]["card_number"] == "1234"
    assert result_data["currency_rates"]["USD"] == 75
    assert result_data["stock_prices"]["AAPL"] == 150