import json
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd
from typing import Tuple
from src.utils import (
    analyze_cards,
    convertation_currency,
    get_greeting,
    get_stocks_prices,
    get_top_five_trans,
    read_xlsx,
)

load_dotenv()
currency_api_key = os.getenv("CURRENCY_API_KEY")
stocks_api_key = os.getenv("STOCKS_API_KEY")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
XLSX_PATH = DATA_DIR / "operations.xlsx"


def get_date_range(input_date: str) -> Tuple[datetime, datetime]:
    """
    Функция, которая принимает дату в формате 'YYYY-MM-DD HH:MM:SS' и возвращает
    диапазон дат (первое число месяца, заданная дата) как объекты datetime
    """
    try:
        date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
        return date.replace(day=1), date
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {input_date}. Ожидается 'YYYY-MM-DD HH:MM:SS'") from e


def main_func(input_date: str, xlsx_path: Path = XLSX_PATH) -> str:
    """
    Главная функция, которая принимает дату в формате 'YYYY-MM-DD HH:MM:SS',
    обрабатывает данные и возвращает результат в формате JSON.
    """
    try:
        # Получаем диапазон дат
        start_date, end_date = get_date_range(input_date)
        date_range_str = f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    except ValueError as e:
        raise ValueError(str(e))

    if not xlsx_path.exists():
        raise FileNotFoundError(f"Файл данных не найден по пути: {xlsx_path}")

    try:
        # Чтение и подготовка данных
        data = pd.read_excel(xlsx_path)

        # Преобразование дат с учетом возможных форматов
        data['Дата операции'] = pd.to_datetime(
            data['Дата операции'],
            dayfirst=True,
            errors='coerce'
        )

        # Проверка на некорректные даты
        if data['Дата операции'].isnull().any():
            bad_dates = data[data['Дата операции'].isnull()]['Дата операции'].tolist()
            raise ValueError(f"Обнаружены некорректные даты: {bad_dates[:5]}...")

        # Фильтрация данных по периоду
        mask = (data['Дата операции'] >= start_date) & (data['Дата операции'] <= end_date)
        filtered_data = data.loc[mask].copy()

        # Обработка данных (ваши функции)
        greeting = f"Отчёт за период: {date_range_str}"
        cards = analyze_cards(data)
        top_transactions = get_top_five_trans(filtered_data)
        currency_rates = convertation_currency(os.getenv("CURRENCY_API_KEY"))
        stock_prices = get_stocks_prices(os.getenv("STOCKS_API_KEY"))

        # Формирование результата
        result = {
            "greeting": greeting,
            "period": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "display": date_range_str
            },
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке данных: {str(e)}")


if __name__ == "__main__":
    try:
        # Пример вызова с правильным форматом даты
        test_date = "31.12.2021"
        print(main_func(test_date))
    except Exception as e:
        print(f"Ошибка: {str(e)}")
