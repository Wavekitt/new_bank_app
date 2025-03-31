import os
from unittest.mock import Mock

import pandas as pd
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def mock_API_KEY():
    return os.getenv("currency_api_key", "mocked_api_key")


@pytest.fixture
def mock_get_stocks_prices_response():
    mock_response = {
        "Global Quote": {
            "05. price": "150.00"
        }
    }
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = mock_response
    return mock


@pytest.fixture
def mock_read_xlsx(mocker):
    return mocker.patch("src.views.read_xlsx", return_value=["mock_data"])


@pytest.fixture
def mock_get_greeting(mocker):
    return mocker.patch("src.views.get_greeting", return_value="Здравствуйте")


@pytest.fixture
def mock_analyze_cards(mocker):
    return mocker.patch("src.views.analyze_cards", return_value=["card_1", "card_2"])


@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [
            "01.03.2019 12:00:00",
            "20.05.2019 03:00:00",
            "15.04.2019 15:30:00",
            "31.08.2019 20:00:00",
        ],
        "Сумма": [100, 200, 300, 400],
    }
    return data


@pytest.fixture
def sample_transactions_data():
    data = {
        "Дата операции": pd.to_datetime([
            "01.01.2025 10:00:00",
            "15.01.2025 12:30:00",
            "01.02.2025 08:00:00",
            "15.03.2025 09:00:00",
            "25.03.2025 14:00:00"
        ], format="%d.%m.%Y %H:%M:%S"),  # Указываем правильный формат
        "Сумма операции": [100, 50, 20, 30, 40],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда", "Транспорт"],
        "Описание": ["Кофе", "Обед", "Такси", "Ужин", "Метро"]
    }
    return pd.DataFrame(data)
