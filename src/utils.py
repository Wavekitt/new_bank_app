import json
import os
import logging
import requests
from dotenv import load_dotenv
from typing import Optional, Any, List, Dict
from datetime import datetime
import pandas as pd


load_dotenv()


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
    operations = pd.read_excel(filepath)
    return operations


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


def convertation_currency(currency: str, rub: str, amount: float) -> Optional[float]:
    """
    Функция, которая конвертирует валюты.
    """
    api_key = os.getenv("API_KEY")  # Получаем ключ из переменной окружения
    if not api_key:
        return None

    url = (
        f"https://api.apilayer.com/exchangerates_data/convert?"
        f"to={rub}&from={currency}&amount={amount}&apikey={api_key}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json().get("result")
        return result
    else:
        return None


def get_top_five_trans(filtered_data: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Функция, которая возвращает топ-5 транзакций по сумме.
    """
    top_five = filtered_data.nlargest(5, "Сумма операции")
    top_list = [
        {
            "date": transactions["Дата операции"].strftime("%d.%m.%Y"),
            "amount": transactions["Сумма операции"],
            "category": transactions["Категория"],
            "description": transactions["Описание"]
        }
        for _, transactions in top_five.iterrows()
    ]
    return top_list


def get_stocks_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """
    Функция, получающая цены на акции.
    """
    stock_prices = []
    try:
        # Получаем API-ключ из переменной окружения
        currency_api_key = os.getenv("API_KEY")
        if not currency_api_key:
            raise ValueError("API key not found in environment variables.")

        logger.info("Функция для получения стоимости акций начала свою работу")
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={currency_api_key}"
            response = requests.get(url, timeout=10, allow_redirects=False)
            if response.status_code == 200:
                logger.info("get запрос на получение цен на акции успешно отправлен")
                data = response.json()
                result = {"stock": stock, "price": round(float(data["Global Quote"]["05. price"]), 2)}
                stock_prices.append(result)
            else:
                logger.error(f"Ошибка API при получении цен на акции: {response.status_code}")
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
