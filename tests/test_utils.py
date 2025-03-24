from unittest.mock import patch
import pandas as pd
from src.utils import (get_greeting, read_xlsx, analyze_cards, convertation_currency,
                       get_top_five_trans, get_stocks_prices, create_json_response)
import os
from dotenv import load_dotenv


load_dotenv()


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


@patch('requests.get')
@patch.dict(os.environ, {"API_KEY": "fake_api_key"})
def test_convert_current_wrong(mock_get):
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"info": {"rate": 100}, "result": 100}
    assert convertation_currency("USD", "RUB", 1.0) == "Error"


def test_get_top_five_trans_success():
    data = {
        "Дата операции": pd.to_datetime(
            ["2025-03-01", "2025-03-02", "2025-03-03", "2025-03-04", "2025-03-05", "2025-03-06"]),
        "Сумма операции": [100, 200, 150, 300, 250, 50],
        "Категория": ["Категория1", "Категория2", "Категория3", "Категория4", "Категория5", "Категория6"],
        "Описание": ["Описание1", "Описание2", "Описание3", "Описание4", "Описание5", "Описание6"]
    }
    df = pd.DataFrame(data)
    result = get_top_five_trans(df)
    assert len(result) == 5
    assert result[0]["amount"] == 300
    assert result[-1]["amount"] == 100


def test_get_stocks_prices_simple(mock_get_stocks_prices_response, mock_API_KEY, mocker):
    mocker.patch('requests.get', return_value=mock_get_stocks_prices_response)
    mocker.patch.dict(os.environ, {"API_KEY": mock_API_KEY})
    stocks = ['AAPL', 'GOOGL']
    result = get_stocks_prices(stocks)
    assert len(result) == 2


def test_create_json_response():
    data = {"name": "John", "age": 30, "city": "New York"}
    expected_result = '''{
    "name": "John",
    "age": 30,
    "city": "New York"
}'''
    result = create_json_response(data)
    assert result == expected_result
