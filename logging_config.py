import logging
import os
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter


def setup_logger(name):
    # Создаём папку для логов
    os.makedirs('logs', exist_ok=True)

    # Формат логов для файлов
    file_format = "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s"

    # Создаём логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Обработчик для инфо-логов
    info_handler = RotatingFileHandler(
        filename=f'logs/{name}_info.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,  # Храним до 3 резервных файлов
        encoding='utf-8'
    )
    info_handler.setLevel(logging.INFO)  # Логи только уровня INFO и выше
    info_handler.setFormatter(logging.Formatter(file_format))
    logger.addHandler(info_handler)

    # Обработчик для ошибок
    error_handler = RotatingFileHandler(
        filename=f'logs/{name}_errors.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)  # Логи только уровня ERROR и выше
    error_handler.setFormatter(logging.Formatter(file_format))
    logger.addHandler(error_handler)

    # Цветной вывод для консоли
    console_format = ColoredFormatter(
        "%(log_color)s[%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # В консоли показываем всё
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger
