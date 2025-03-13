import pandas as pd
import json
from datetime import datetime


def get_greeting():
    """
    Функция, которая определяет текущее время и судя по нему выводит приветствие
    """
    time_now = datetime.now().time()
    morning_time_start = datetime.strptime("06:00:00", "%H:%M:%S").time()
    morning_time_end = datetime.strptime("11:59:59", "%H:%M:%S").time()
    day_time_start = datetime.strptime("12:00:00", "%H:%M:%S").time()
    day_time_end = datetime.strptime("17:59:59", "%H:%M:%S").time()
    evening_time_start = datetime.strptime("18:00:00", "%H:%M:%S").time()
    evening_time_end = datetime.strptime("22:59:59", "%H:%M:%S").time()

    # Проверяем, в какой диапазон попадает текущее время
    if morning_time_start <= time_now <= morning_time_end:
        return "Доброе утро"
    elif day_time_start <= time_now <= day_time_end:
        return "Добрый день"
    elif evening_time_start <= time_now <= evening_time_end:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_xlsx(filepath):
    """
    Функция, которая читает exel файл
    """
    operations = pd.read_excel(filepath)
    return operations


def analyze_cards(df):
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


def main(file_path):
    """
    Главная функция для обработки данных из Excel и формирования JSON-ответа.
    """
    df = read_xlsx(file_path)
    greeting = get_greeting()
    cards_data = analyze_cards(df)
    result = {
        "greeting": greeting,
        "cards": cards_data
    }
    return json.dumps(result, ensure_ascii=False, indent=4)


file_path = r"C:\Users\wavekitt\new_bank_app\data\operations.xlsx"
print(main(file_path))


# if __name__ == "__main__":
#     excel_file = r"C:\Users\wavekitt\new_bank_app\data\operations.xlsx"
#     read_file = read_xlsx(excel_file)
#     print(read_file)
