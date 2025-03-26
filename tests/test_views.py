import json
from unittest.mock import MagicMock, patch

import pytest

from src.views import get_date_range, main_func


@pytest.mark.parametrize("input_date, expected_output", [
    ("15.03.2025", "01.03.2025 - 15.03.2025"),
    ("01.01.2025", "01.01.2025 - 01.01.2025"),
])
def test_get_date_range(input_date, expected_output):
    assert get_date_range(input_date) == expected_output, "Функция должна возвращать правильный диапазон дат."


@patch('src.views.read_xlsx')  # Мок для read_xlsx
@patch('src.views.get_greeting', return_value="Добрый день")  # Мок для get_greeting
@patch('src.views.analyze_cards', return_value=[{"card_number": "1234", "total_expenses": 1000}])
@patch('src.views.get_top_five_trans', return_value=[])  # Мок для get_top_five_trans
@patch('src.views.convertation_currency', return_value={"USD": 75, "EUR": 85})  # Мок для convertation_currency
@patch('src.views.get_stocks_prices', return_value={"AAPL": 150, "TSLA": 700})  # Мок для get_stocks_prices
def test_main_func(mock_get_stocks_prices, mock_convertation_currency, mock_top_five, mock_analyze_cards,
                   mock_greeting, mock_read_xlsx):
    input_date = "2023-10-15 12:00:00"  # Пример передаваемой даты

    # Настройка мока для read_xlsx
    mock_read_xlsx.return_value = MagicMock()  # Можно вернуть фиктивный DataFrame или MagicMock

    # Вызов функции с передачей input_date
    result = main_func(input_date)

    # Проверка результата
    expected_result = {
        "greeting": "Добрый день",
        "cards": [{"card_number": "1234", "total_expenses": 1000}],
        "top_transactions": [],
        "currency_rates": {"USD": 75, "EUR": 85},
        "stock_prices": {"AAPL": 150, "TSLA": 700}
    }

    # Проверка, что результат совпадает с ожидаемым
    assert json.loads(result) == expected_result

    # Проверка, что моки были вызваны
    mock_read_xlsx.assert_called_once()
    mock_greeting.assert_called_once()
    mock_analyze_cards.assert_called_once()
    mock_top_five.assert_called_once()
    mock_convertation_currency.assert_called_once()
    mock_get_stocks_prices.assert_called_once()
