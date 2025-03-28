import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()

currency_api_key = os.getenv("CURRENCY_API_KEY")
stocks_api_key = os.getenv("STOCKS_API_KEY")

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)


logger = logging.getLogger("utils")
file_handler = logging.FileHandler(os.path.join(logs_dir, "utils.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting() -> str:
    """
    Функция, которая определяет текущее время и судя по нему выводит приветствие.
    """
    time_now = datetime.now().time()
    morning_time_start = datetime.strptime("06:00:00", "%H:%M:%S").time()
    morning_time_end = datetime.strptime("11:59:59", "%H:%M:%S").time()
    day_time_start = datetime.strptime("12:00:00", "%H:%M:%S").time()
    day_time_end = datetime.strptime("17:59:59", "%H:%M:%S").time()
    evening_time_start = datetime.strptime("18:00:00", "%H:%M:%S").time()
    evening_time_end = datetime.strptime("22:59:59", "%H:%M:%S").time()

    if morning_time_start <= time_now <= morning_time_end:
        return "Доброе утро"
    elif day_time_start <= time_now <= day_time_end:
        return "Добрый день"
    elif evening_time_start <= time_now <= evening_time_end:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_xlsx(filepath: str) -> pd.DataFrame:
    """
    Функция, которая читает Excel файл.
    """
    df = pd.read_excel(filepath)  # Используем pd.read_excel для чтения файла
    return df


def analyze_cards(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Анализ данных по картам, расчёт общей суммы, кэшбэка и последних 4 цифр номера карты.
    """
    result = []
    grouped = df.groupby("Номер карты").agg({
        "Сумма операции": "sum",
        "Кэшбэк": "sum"
    }).reset_index()

    for _, row in grouped.iterrows():
        card_info = {
            "card_number": str(row["Номер карты"])[-4:],
            "total_expenses": row["Сумма операции"],
            "cashback": row["Кэшбэк"]
        }
        result.append(card_info)
    return result


def convertation_currency(currencies: list) -> Any:
    """
    Конвертирует валюту через API.
    Возвращает сумму или "Error" при ошибке.
    """
    try:
        logger.info("Функция конвертации валют начала свою работу")
        currency_rates = []
        for currency in currencies:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            headers = {"apikey": currency_api_key}
            params = {"from": currency, "to": "RUB", "amount": 1}
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                logger.info("get запрос на получение курса валют успешно отправлен")
                data = response.json()
                result = {"currency": currency, "rate": round(float(data["result"]), 2)}
                currency_rates.append(result)
            else:
                logger.error(f"Ошибка API при получении курса валют: {response.status_code}")
                print(f"Ошибка API: {response.status_code}")
                return []
        if currency_rates:
            logger.info("Конвертация валют прошла успешно")
            return currency_rates
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        logger.error(f"Ошибка при конвертации: {e}")
        return []


def get_top_five_trans(filtered_df: pd.DataFrame) -> list[dict]:
    """Функция для получения топ транзакций по сумме платежа"""
    try:
        logger.info("Функция по получению топ транзакций начала свою работу")
        top_5_transactions = filtered_df.nlargest(5, "Сумма операции")
        top_list = [
            {
                "date": transaction["Дата операции"].strftime("%y.%m.%d"),
                "amount": transaction["Сумма операции"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
            for _, transaction in top_5_transactions.iterrows()
        ]
        logger.info("Функция по получению топ транзакций успешно завершила свою работу")
        return top_list
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []


def get_stocks_prices(stocks: list) -> Any:
    """
    Функция, получающая цены на акции.
    """
    stock_prices = []
    try:
        logger.info("Функция для получения стоимости акций начала свою работу")
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={stocks_api_key}"
            response = requests.get(url, timeout=10, allow_redirects=False)
            if response.status_code == 200:
                logger.info("get запрос на получение цен на акции успешно отправлен")
                data = response.json()
                result = {"stock": stock, "price": round(float(data["Global Quote"]["05. price"]), 2)}
                stock_prices.append(result)
            else:
                logger.error(f"Ошибка API при получении цен на акции: {response.status_code}")
                print(f"Ошибка API: {response.status_code}")
                return []
        if stock_prices:
            logger.info("Операция по получению цен на акции прошла успешно")
            return stock_prices
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []


def create_json_response(python_str: Any) -> str:
    """
    Функция для формирования строки json.
    """
    json_data = json.dumps(python_str, indent=4, ensure_ascii=False)
    return json_data
