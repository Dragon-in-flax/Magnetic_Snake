# Класс Food — еда с дрейфом и магнитным притяжением к змейке
import math
import random
import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    FOOD_RADIUS, FOOD_DRIFT_SPEED,
    MAGNET_RADIUS, MAGNET_ACCEL, MAGNET_MAX_SPEED,
    COLORS,
)


class Food:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        # Случайное направление свободного дрейфа
        a = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(a) * FOOD_DRIFT_SPEED
        self.vy = math.sin(a) * FOOD_DRIFT_SPEED

        self.radius = FOOD_RADIUS
        self.is_attracted = False   # для визуального свечения

    def update(self, snake):
        # Дрейф + магнитное притяжение к голове змейки
        # --- 1. Свободный дрейф с отскоком от стен ---
        self.x += self.vx
        self.y += self.vy

        if self.x < self.radius or self.x > WINDOW_WIDTH - self.radius:
            self.vx = -self.vx
            self.x = max(self.radius, min(WINDOW_WIDTH - self.radius, self.x))
        if self.y < self.radius or self.y > WINDOW_HEIGHT - self.radius:
            self.vy = -self.vy
            self.y = max(self.radius, min(WINDOW_HEIGHT - self.radius, self.y))

        # --- 2. Магнитное притяжение ---
        dx = snake.x - self.x
        dy = snake.y - self.y
        dist = math.hypot(dx, dy)

        if 0.001 < dist < MAGNET_RADIUS:
            self.is_attracted = True
            # Единичный вектор от еды к голове
            nx, ny = dx / dist, dy / dist
            # Чем ближе — тем сильнее (линейный закон)
            force = MAGNET_ACCEL * (1.0 - dist / MAGNET_RADIUS)
            self.vx += nx * force
            self.vy += ny * force

            # Ограничение скорости
            sp = math.hypot(self.vx, self.vy)
            if sp > MAGNET_MAX_SPEED:
                self.vx = self.vx / sp * MAGNET_MAX_SPEED
                self.vy = self.vy / sp * MAGNET_MAX_SPEED
        else:
            self.is_attracted = False

    def check_eaten(self, snake) -> bool:
        dx, dy = snake.x - self.x, snake.y - self.y
        return math.hypot(dx, dy) < (snake.radius + self.radius)

    def draw(self, surface: pygame.Surface):
        cx, cy = int(self.x), int(self.y)
        if self.is_attracted:
            pygame.draw.circle(surface, COLORS["food_glow"],
                               (cx, cy), self.radius + 6, 2)
        pygame.draw.circle(surface, COLORS["food"], (cx, cy), self.radius)
        # Блик
        pygame.draw.circle(surface, (255, 220, 220),
                           (cx - 2, cy - 2), max(2, self.radius // 3))