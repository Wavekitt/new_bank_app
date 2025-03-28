import logging
import os
from pathlib import Path
from datetime import datetime
from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import read_xlsx
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
    try:
        # Загрузка данных
        data_path = Path(__file__).parent.parent / "data" / "operations.xlsx"
        df = read_xlsx(data_path)
        logger.info("Данные успешно загружены из %s", data_path)

        print(
            """
Выберите категорию для отображения:
1. Главная страница
2. Сервис Инвесткопилка
3. Отчет траты по категории
        """
        )

        while True:
            menu = input("Введите номер категории: \n")
            logger.info("Пользователь выбрал: %s", menu)

            if menu == "1":
                logger.info("Обработка главной страницы")
                while True:
                    input_date = input("Введите дату в формате 'ДД.ММ.ГГГГ ЧЧ:ММ:СС'\n")
                    try:
                        # Преобразуем в нужный формат перед передачей в main_func
                        dt = datetime.strptime(input_date, "%d.%m.%Y %H:%M:%S")
                        iso_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                        result = main_func(iso_date)
                        print(result)
                        break
                    except ValueError:
                        print("Ошибка формата. Пример: 31.12.2021 16:44:00")
                        logger.warning("Некорректный ввод даты: %s", input_date)

            elif menu == "2":
                logger.info("Обработка Инвесткопилки")
                while True:
                    month = input("Введите месяц в формате: 'ГГГГ-ММ'\n")
                    try:
                        limit = int(input("Введите лимит: 10/50/100\n"))
                        if limit not in (10, 50, 100):
                            raise ValueError
                        transacts_list = df.to_dict(orient="records")
                        print(investment_bank(month, transacts_list, limit))
                        logger.info("Успешный вывод Инвесткопилки")
                        break
                    except ValueError:
                        print("Некорректный ввод. Пример месяца: 2023-12. Лимит: 10, 50 или 100.")
                        logger.warning("Некорректный ввод для Инвесткопилки")

            elif menu == "3":
                logger.info("Обработка отчета по категориям")
                category = input("Введите категорию трат: \n")
                date = input(
                    "Введите дату в формате 'ДД.ММ.ГГГГ ЧЧ:ММ:СС' (или Enter для текущей даты):\n"
                )
                print(spending_by_category(df, category, date or None))
                logger.info("Успешный вывод отчета по категориям")

            else:
                print("Некорректный ввод. Введите 1, 2 или 3.\n")
                continue

            break

    except FileNotFoundError:
        logger.error("Файл данных не найден: %s", data_path)
        print("Ошибка: файл данных не найден. Проверьте наличие operations.xlsx")
    except Exception as e:
        logger.error("Критическая ошибка: %s", str(e), exc_info=True)
        print(f"Произошла ошибка: {e}. Подробности в логе.")


if __name__ == "__main__":
    main()