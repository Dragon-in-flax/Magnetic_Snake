# --- Окно ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# --- Параметры змейки ---
SNAKE_SPEED = 3.0            # пикселей за кадр
SNAKE_TURN_SPEED = 4.0       # градусов за кадр (A / D)
SNAKE_HEAD_RADIUS = 10
SNAKE_SEGMENT_RADIUS = 8
SNAKE_START_LENGTH = 5
SEGMENT_SPACING = 8          # через сколько "кадров истории" стоит след. сегмент

# --- Магнетизм ---
MAGNET_RADIUS = 150          # радиус притяжения еды (px)
MAGNET_ACCEL = 0.6           # ускорение притяжения
MAGNET_MAX_SPEED = 8.0       # ограничение скорости еды

# --- Еда ---
FOOD_RADIUS = 8
FOOD_DRIFT_SPEED = 1.0       # скорость свободного дрейфа еды
FOOD_SPAWN_MARGIN = 40       # отступ от стен при спавне

# --- Цвета ---
COLORS = {
    "bg":           (65, 5, 10), # 38, 221, 255 | 15, 15, 25
    "grid":         (110, 0, 10), # 25, 25, 40
    "snake_head":   (55, 155, 255), # 80, 220, 120
    "snake_body":   (55, 155, 255), # 40, 160, 90
    "snake_glow":   (200, 50, 50), # 120, 255, 160
    "food":         (255, 90, 90),
    "food_glow":    (195, 165, 0), # 255, 160, 160
    "magnet_field": (195, 165, 0), # 60, 100, 180
    "text":         (240, 240, 250),
    "text_dim":     (150, 150, 170),
    "accent":       (120, 200, 255),
    "game_over":    (255, 80, 80),
}

# --- Состояния игры ---
STATE_MENU = "MENU"
STATE_PLAY = "PLAY"
STATE_GAME_OVER = "GAME_OVER"

# --- Игровой счёт ---
SCORE_PER_FOOD = 10
