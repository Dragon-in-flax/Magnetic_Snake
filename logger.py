"""Модуль для настройки логирования игровых событий."""
import logging

def setup_logger():
    # Пишет в файл snake_game.log с указанием времени
    logging.basicConfig(
        filename='snake_game.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8' # Для русского языка в логах
    )
    return logging.getLogger(__name__)