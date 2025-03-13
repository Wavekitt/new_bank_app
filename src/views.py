import datetime


def get_date_range(input_date: str) -> str:
    """
    Функция, которая принимает дату и выводит с 1 числа заданного месяца, по заднный день
    """
    date = datetime.datetime.strptime(input_date, "%d.%m.%Y")
    start_date = date.replace(day=1)
    start_date_str = start_date.strftime("%d.%m.%Y")
    end_date_str = date.strftime("%d.%m.%Y")
    return f"{start_date_str} - {end_date_str}"


print(get_date_range("10.02.2025"))