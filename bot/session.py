import json
from config import SESSION_DIR

def load_session(user_id: int) -> dict:
    path = SESSION_DIR / f"{user_id}.json"
    if not path.exists():
        return {"name": "Игрок", "screen_id": None}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"name": "Игрок", "screen_id": None}

def save_session(user_id: int, data: dict):
    path = SESSION_DIR / f"{user_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)