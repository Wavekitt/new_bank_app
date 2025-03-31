import logging
import os
from functools import wraps
from typing import Any, Callable, Optional

# Настройка логирования
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(logs_dir, exist_ok=True)

logger = logging.getLogger("decorators")
file_handler = logging.FileHandler(os.path.join(logs_dir, "decorators.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def report_func(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для записи отчета в файл.
    Записывает как успешный результат работы функции, так и ошибки с подробностями.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info("Определение файла для декоратора")
            report_dir = "../reports"
            if filename:
                logger.info("Работа с переданным файлом для записи")
                report_dir = os.path.dirname(filename)
                os.makedirs(report_dir, exist_ok=True)
            else:
                logger.info("Работа с дефолтным файлом для записи")
                os.makedirs(report_dir, exist_ok=True)

            try:
                logger.info("Вызов функции внутри декоратора")
                result = func(*args, **kwargs)
                report_message = f"Результат функции {func.__name__}: {result}\n"
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(report_message)
                else:
                    with open(os.path.join(report_dir, "report.log"), "w", encoding="utf-8") as file:
                        file.write(report_message)
                logger.info("Запись в файл результата успешной работы функции")
                return result
            except Exception as error:
                logger.error("Ошибка при выполнении функции", exc_info=True)
                report_message = (
                    f"{func.__name__} error: {error.__class__.__name__}. "
                    f"Inputs: {args}, {kwargs}\n"
                )
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(report_message)
                else:
                    with open(os.path.join(report_dir, "report.log"), "w", encoding="utf-8") as file:
                        file.write(report_message)
                logger.info("Запись в файл об ошибке работы функции")
                raise error  # Перебрасываем ошибку после записи

        return wrapper

    return decorator
