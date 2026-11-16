import csv
import re
from config import CSV_FILE, LOG_FILE

def get_top(limit=5):
    """Читает CSV (Имя; Очки; Дата) и возвращает топ-5."""
    if not CSV_FILE.exists(): return []
    records = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None) # пропускает заголовок
        for row in reader:
            if len(row) >= 2:
                records.append((row[0], int(row[1])))
    records.sort(key=lambda x: x[1], reverse=True)
    return records[:limit]

def get_stats(player_name: str):
    """Ищет лучший результат игрока."""
    if not CSV_FILE.exists(): return None
    best_score = 0
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if len(row) >= 2 and row[0] == player_name:
                best_score = max(best_score, int(row[1]))
    return best_score

def get_achievements(score: int):
    achievements = []
    if score >= 10: achievements.append("🥉 Новичок (10+ очков)")
    if score >= 50: achievements.append("🥈 Магнитный лорд (50+ очков)")
    if score >= 100: achievements.append("🥇 Повелитель змей (100+ очков)")
    return achievements