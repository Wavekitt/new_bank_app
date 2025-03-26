import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.decorators import report_func

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(os.path.join(logs_dir, "reports.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


@report_func("../reports/report.log")
def spending_by_category(
        transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> str:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    logger.info("Начало работы функции траты по категориям")
    category = category.capitalize()

    # Определяем дату
    if date:
        input_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    else:
        input_date = datetime.now()

    logger.info("Определение времени для работы с транзакциями")

    # Преобразуем столбец с датами в тип datetime
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Определяем дату три месяца назад
    three_month_ago = input_date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    filtered_df = transactions[(
        transactions["Категория"] == category
        ) & (transactions["Дата операции"] >= three_month_ago)
        & (transactions["Дата операции"] <= input_date)
        & (transactions["Сумма операции"] < 0)
    ]

    # Переводим транзакции в список словарей
    transacts_dict = filtered_df.to_dict(orient="records")

    # Преобразуем даты в строки
    for record in transacts_dict:
        record["Дата операции"] = record["Дата операции"].strftime("%d.%m.%Y %H:%M:%S")

    return json.dumps(transacts_dict, ensure_ascii=False, indent=4)
