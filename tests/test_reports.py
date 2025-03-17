import pytest
import pandas as pd
from src.reports import spending_by_category
from src.utils import read_xlsx
from src.decorators import report_func
import pandas as pd
import json


def test_spending_by_category_with_transactions(sample_transactions):
    category = "Еда"
    date = "25.03.2025 14:00:00"
    result = spending_by_category(sample_transactions, category, date)
    result_dict = json.loads(result)
    assert len(result_dict) == 3
    for item in result_dict:
        assert item["Категория"] == "Еда"
    assert result_dict[0]["Дата операции"] == "01.01.2025 10:00:00"
