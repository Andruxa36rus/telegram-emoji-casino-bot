import logging
import os
from datetime import datetime


def setup_logger(log_dir):
    """Настройка системы логирования"""
    os.makedirs(log_dir, exist_ok=True)

    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Логгер для победителей
    winners_logger = logging.getLogger('winners')
    winners_logger.setLevel(logging.INFO)
    winners_handler = logging.FileHandler(log_dir / f"winners.log", encoding='utf-8')
    winners_handler.setFormatter(logging.Formatter('%(message)s'))
    winners_logger.addHandler(winners_handler)

    # Логгер для ошибок
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.ERROR)
    error_file_handler = logging.FileHandler(log_dir / f"error.log", encoding='utf-8')
    error_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    error_stream_handler = logging.StreamHandler()
    error_stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    error_logger.addHandler(error_file_handler)
    error_logger.addHandler(error_stream_handler)

    return winners_logger, error_logger