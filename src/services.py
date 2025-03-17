import logging
import os
from datetime import datetime
from typing import Any, Dict, List
from src.utils import create_json_response


logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)


logger = logging.getLogger("services")
file_handler = logging.FileHandler(os.path.join(logs_dir, "services.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """
    Функция, которая возвращает сумму, которую удалось бы отложить в «Инвесткопилку».

    :param month: Месяц в формате "ГГГГ-ММ".
    :param transactions: Список транзакций с датами и суммами.
    :param limit: Пороговая сумма для округления.
    :return: JSON строка с результатом.
    """
    try:
        logger.info("Функция для «Инвесткопилки» начала свою работу")
        total_saved = 0.0
        target_month = datetime.strptime(month, "%Y-%m")

        for transact in transactions:
            transact_date = datetime.strptime(transact["Дата операции"], "%d.%m.%Y %H:%M:%S")

            if transact_date.year == target_month.year and transact_date.month == target_month.month:
                amount = transact["Сумма операции"]
                rounded_amount = ((amount + limit - 1) // limit) * limit
                saved_amount = rounded_amount - amount
                total_saved += saved_amount

        logger.info(f"Общая сумма сбережений за месяц {month}: {total_saved} ₽")
        final_str = {"Сумма, отложенная в «Инвесткопилку»": round(total_saved, 2)}
        json_data = create_json_response(final_str)
        return json_data
    except ValueError:
        logger.error("Месяц должен быть указан в формате 'ГГГГ-ММ'")
        raise ValueError("Месяц должен быть указан в формате 'ГГГГ-ММ'")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return "0.0"
