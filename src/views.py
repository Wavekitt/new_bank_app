import datetime
import json
from src.utils import analyze_cards, read_xlsx, get_greeting
from typing import Dict, Any


def get_date_range(input_date: str) -> str:
    """
    Функция, которая принимает дату и выводит с 1 числа заданного месяца,
    по заданный день.
    """
    date = datetime.datetime.strptime(input_date, "%d.%m.%Y")
    start_date = date.replace(day=1)
    start_date_str = start_date.strftime("%d.%m.%Y")
    end_date_str = date.strftime("%d.%m.%Y")
    return f"{start_date_str} - {end_date_str}"


def main_func() -> str:
    """
    Главная функция для обработки данных из Excel и формирования JSON-ответа.
    """
    file_path = "../data/operations.xlsx"
    df = read_xlsx(file_path)
    greeting = get_greeting()
    cards_data = analyze_cards(df)
    result: Dict[str, Any] = {
        "greeting": greeting,
        "cards": cards_data
    }
    return json.dumps(result, ensure_ascii=False, indent=4)