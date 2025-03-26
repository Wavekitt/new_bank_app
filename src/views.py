import json
from datetime import datetime

from src.utils import (
    analyze_cards,
    convertation_currency,
    get_greeting,
    get_stocks_prices,
    get_top_five_trans,
    read_xlsx,
)


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


def main_func(input_date: str) -> str:
    """
    Главная функция, которая принимает дату в формате 'YYYY-MM-DD HH:MM:SS',
    обрабатывает данные и возвращает результат в формате JSON.
    """
    try:
        # Преобразуем строку в объект datetime
        date_object = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Некорректный формат даты. Используйте 'YYYY-MM-DD HH:MM:SS'.")
    start_of_month = date_object.replace(day=1)
    try:
        data = read_xlsx(input_date)  # Предположим, что input_date - это путь к файлу
        greeting = get_greeting()
        cards = analyze_cards(data)
        top_transactions = get_top_five_trans(start_of_month, date_object)
        currency_rates = convertation_currency()  # Получаем курсы валют
        stock_prices = get_stocks_prices()  # Получаем цены акций
    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке данных: {str(e)}")
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    return json.dumps(result)
