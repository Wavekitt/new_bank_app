import json

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_with_transactions():
    sample_transactions = pd.DataFrame([
        {"Дата операции": "01.03.2025 10:00:00", "Сумма операции": -150, "Категория": "Еда"},
        {"Дата операции": "15.03.2025 15:30:00", "Сумма операции": -200, "Категория": "Еда"},
        {"Дата операции": "25.03.2025 12:45:00", "Сумма операции": -80, "Категория": "Еда"},
        {"Дата операции": "10.02.2025 16:00:00", "Сумма операции": -100, "Категория": "Транспорт"}
        # Добавим запись за февраль для проверки границы
    ])

    category = "Еда"
    date = "25.03.2025 14:00:00"
    result = spending_by_category(sample_transactions, category, date)
    result_dict = json.loads(result)

    print(result_dict)  # Для отладки

    assert len(result_dict) == 3
    for item in result_dict:
        assert item["Категория"] == "Еда"
        assert item["Сумма операции"] < 0
