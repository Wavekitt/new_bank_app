from datetime import datetime
import json
from src.utils import (read_xlsx, get_greeting, analyze_cards, get_top_five_trans)


def get_date_range(input_date: str) -> str:
    """
    Функция, которая принимает дату в формате 'дд.мм.гггг' и выводит диапазон
    с 1 числа заданного месяца по заданный день.
    """
    # Преобразуем строку в объект datetime
    date = datetime.strptime(input_date, "%d.%m.%Y")  # Исправлен формат даты
    start_date = date.replace(day=1)  # Первое число месяца
    start_date_str = start_date.strftime("%d.%m.%Y")  # Форматируем в 'дд.мм.гггг'
    end_date_str = date.strftime("%d.%m.%Y")  # Форматируем в 'дд.мм.гггг'
    return f"{start_date_str} - {end_date_str}"


def main_func() -> str:
    input_date = input("Введите дату в формате: 'YYYY-MM-DD HH:MM:SS'\n")

    try:
        # Преобразуем строку в объект datetime
        date_object = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Некорректный формат даты. Используйте 'YYYY-MM-DD HH:MM:SS'.")

    start_of_month = date_object.replace(day=1)

    # Получаем данные и выполняем необходимые операции
    data = read_xlsx(input_date)
    greeting = get_greeting()
    cards = analyze_cards(data)
    top_transactions = get_top_five_trans(start_of_month, date_object)

    # Формируем результат (без currency_rates и stock_prices)
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions
    }

    return json.dumps(result)
