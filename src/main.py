import logging
import os
from src.reports import spending_by_category
from src.services import investment_bank, read_xlsx
from src.views import main_func


logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger("main")
file_handler = logging.FileHandler(os.path.join(logs_dir, "main.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main() -> None:
    """
    Главная функция для отображения меню и взаимодействия с пользователем.
    """
    df = read_xlsx("../data/operations.xlsx")
    logger.info("Начало работы главной функции. Вывод меню для выбора пользователю")

    print(
        """
Выберите категорию для отображения:
1. Главная страница
2. Сервис Инвесткопилка
3. Отчет траты по категории
        """
    )

    menu = ""
    while menu not in ("1", "2", "3"):
        menu = input("Введите номер категории: \n")
        logger.info("Пользователь выбирает категорию в меню")

        if menu not in ("1", "2", "3"):
            print("Некорректный ввод. Введите 1, 2 или 3. \n")
            logger.info("Введен некорректный ввод")

    # В зависимости от выбора, выполняются разные действия
    if menu == "1":
        logger.info("Выбрана категория Главная страница для отображения")
        print("Главная страница")
        input_date = input("Введите дату в формате: 'ДД.ММ.ГГГГ ЧЧ:ММ:СС'\n")

        # Используем input_date в main_func
        result = main_func(input_date)  # Предполагается, что main_func принимает input_date
        print(result)
        logger.info("Вывод результата программы")

    elif menu == "2":
        logger.info("Выбрана категория Инвесткопилка для отображения")
        print("Выбран сервис, который возвращает сумму, которую удалось бы отложить в Инвесткопилку\n")

        month = input("Введите месяц в формате: 'ГГГГ-ММ'\n")
        limit = int(input("Введите лимит: 10/50/100\n"))

        # Преобразуем DataFrame в список словарей
        transacts_list = df.to_dict(orient="records")

        # Вызываем сервис инвестиционной копилки
        print(investment_bank(month, transacts_list, limit))

        logger.info("Вывод результата программы")

    elif menu == "3":
        logger.info("Выбрана категория Отчеты по категории для отображения")
        print("Выбран отчет траты по категории")

        category = input("Введите категорию трат: \n")
        date = input(
            "При вводе некорректной даты будет использована текущая дата.\n"
            "Введите дату в формате 'ДД.ММ.ГГГГ ЧЧ:ММ:СС' для формирования отчета:\n"
        )
        print(spending_by_category(df, category, date))
        logger.info("Вывод результата ")
