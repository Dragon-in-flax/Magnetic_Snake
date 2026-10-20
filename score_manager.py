import csv
import os
from datetime import datetime

CSV_FILE = "snake_records.csv"

def save_score(name, score):
    """Сохраняет результат игрока в CSV-файл."""
    # Проверяем, существует ли файл (если нет — запишем заголовки)
    file_exists = os.path.exists(CSV_FILE)
    
    # Открываем файл в режиме 'a' (append - дописывание)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';') # Используем ; для лучшей читаемости в Excel
        
        if not file_exists:
            writer.writerow(["Имя", "Очки", "Дата"])
            
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        writer.writerow([name, score, now])

def get_top_5():
    """Читает CSV и возвращает топ-5 игроков."""
    if not os.path.exists(CSV_FILE):
        return []
        
    records = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None) # Пропускаем заголовок
        for row in reader:
            if len(row) == 3:
                records.append((row[0], int(row[1]))) # Имя и очки
                
    # Сортируем по очкам (по убыванию) и берем первые 5
    records.sort(key=lambda x: x[1], reverse=True)
    return records[:5]