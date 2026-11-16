import os
from pathlib import Path
from dotenv import load_dotenv

# Указывает точный путь к папке, где лежит этот файл (папка bot)
BASE_DIR = Path(__file__).resolve().parent
# Загружает .env именно оттуда
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("BOT_TOKEN")

# Пути к файлам из ЛР2 (они лежат в корне, на уровень выше папки bot)
ROOT_DIR = BASE_DIR.parent 
CSV_FILE = ROOT_DIR / "snake_records.csv"
LOG_FILE = ROOT_DIR / "snake_game.log"

# Папка для сессий
SESSION_DIR = BASE_DIR / "sessions"
SESSION_DIR.mkdir(exist_ok=True)