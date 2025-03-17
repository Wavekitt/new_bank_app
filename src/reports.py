import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
from src.utils import read_xlsx
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

    :param transactions: DataFrame с транзакциями.
    :param category: Категория расходов.
    :param date: Дата, с которой нужно начинать анализ (если не передана, берется текущая дата).
    :return: JSON строка с данными о расходах.
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
    transactions["Дата операции"] = transactions["Дата операции"].apply(
        lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S") if pd.notnull(x) else None
    )

    # Определяем дату три месяца назад
    three_month_ago = input_date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    filtered_df = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_month_ago)
        & (transactions["Дата операции"] <= input_date)
        & (transactions["Сумма платежа"] < 0)
        ]
    logger.info("Транзакции переводятся в список словарей для дальнейшей работы")

    # Переводим транзакции в список словарей
    transacts_dict = filtered_df.to_dict(orient="records")
    final_list = []

    for item in transacts_dict:
        item["Дата операции"] = item["Дата операции"].strftime("%d.%m.%Y %H:%M:%S")
        final_list.append(item)

    logger.info(f"Формирование итогового списка транзакций. Всего: {len(final_list)} транзакций")
    logger.info("Завершение работы функции. Формирование итоговой JSON строки")

    return json.dumps(final_list, ensure_ascii=False, indent=4)
