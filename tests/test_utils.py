import os
from unittest.mock import patch, mock_open

import pandas as pd
from dotenv import load_dotenv

from src.utils import (
    analyze_cards,
    convertation_currency,
    create_json_response,
    get_greeting,
    get_stocks_prices,
    get_top_five_trans,
    read_xlsx,
)

load_dotenv()

currency_url = "https://api.apilayer.com/exchangerates_data/convert"
currency_api_key = os.getenv("CURRENCY_API_KEY")
headers = {"apikey": currency_api_key}


def test_get_greeting():
    greeting = get_greeting()
    assert greeting in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


def test_read_xlsx(tmp_path):
    filepath = tmp_path / "test.xlsx"
    df = pd.DataFrame({"Номер карты": [1234], "Сумма операции": [1000], "Кэшбэк": [50]})
    df.to_excel(filepath, index=False)
    result = read_xlsx(filepath)
    assert result.equals(df)


def test_analyze_cards():
    df = pd.DataFrame({"Номер карты": [1234, 5678], "Сумма операции": [1000, 2000], "Кэшбэк": [50, 100]})
    result = analyze_cards(df)
    assert len(result) == 2
    assert result[0]["card_number"] == "1234"
    assert result[1]["total_expenses"] == 2000


@patch("builtins.open", mock_open(read_data='{"currencies": ["USD"]}'))
@patch("requests.get")
def test_convertation_currency_simple(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 75.50}
    result = convertation_currency()
    assert result == [{"currency": "USD", "rate": 75.5}]


def test_get_top_five_trans(sample_transactions_data):
    expected_result = [
        {"date": "25.01.01", "amount": 100, "category": "Еда", "description": "Кофе"},
        {"date": "25.01.15", "amount": 50, "category": "Еда", "description": "Обед"},
        {"date": "25.03.25", "amount": 40, "category": "Транспорт", "description": "Метро"},
        {"date": "25.03.15", "amount": 30, "category": "Еда", "description": "Ужин"},
        {"date": "25.02.01", "amount": 20, "category": "Транспорт", "description": "Такси"},
    ]
    result = get_top_five_trans(sample_transactions_data)
    assert result == expected_result


@patch("builtins.open", mock_open(read_data='{"stocks": ["AAPL"]}'))
@patch("requests.get")
def test_get_stocks_prices_api_error(mock_get):
    mock_get.return_value.status_code = 500
    result = get_stocks_prices()
    assert result == []


def test_create_json_response():
    data = {"name": "John", "age": 30, "city": "New York"}
    expected_result = '''{
    "name": "John",
    "age": 30,
    "city": "New York"
}'''
    result = create_json_response(data)
    assert result == expected_result
