"""Модуль для загрузки настроек из JSON."""
import json
import os

def load_settings(filepath="snake_settings.json"):
    # Настройки по умолчанию (если файл потеряется)
    defaults = {
        "snake_speed": 3.0,
        "magnet_radius": 150,
        "magnet_accel": 0.6,
        "food_drift_speed": 1.0
    }

    if not os.path.exists(filepath):
        print(f"Файл {filepath} не найден. Используются настройки по умолчанию.")
        return defaults

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            settings = json.load(f)
            # Объединяем дефолтные настройки с загруженными (на случай, если в файле не хватает ключа)
            return {**defaults, **settings}
    except Exception as e:
        print(f"Ошибка чтения настроек: {e}. Используются настройки по умолчанию.")
        return defaults