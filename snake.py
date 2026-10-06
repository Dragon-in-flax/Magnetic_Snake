
"""Класс Snake — змейка со свободной траекторией (не по сетке).

Идея:
    Голова — точка (x, y), которая движется под углом self.angle.
    Тело — это "история" позиций головы: сегмент №i находится там,
    где голова была i*SEGMENT_SPACING кадров назад.
"""
import math
import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SNAKE_SPEED, SNAKE_TURN_SPEED,
    SNAKE_HEAD_RADIUS, SNAKE_SEGMENT_RADIUS,
    SNAKE_START_LENGTH, SEGMENT_SPACING,
    COLORS,
)


class Snake:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.angle = 0.0                 # 0° — вправо, растёт по часовой
        self.speed = SNAKE_SPEED
        self.radius = SNAKE_HEAD_RADIUS
        self.length = SNAKE_START_LENGTH
        self.alive = True

        # История позиций головы: [0] — текущая, [n] — старая
        self.history = [(self.x, self.y)]

    def turn(self, direction: int):
        # direction = -1 — влево (A), +1 — вправо (D)
        self.angle = (self.angle + direction * SNAKE_TURN_SPEED) % 360

    def update(self):
        # Движение головы по тригонометрии
        if not self.alive:
            return

        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

        # Запоминаем позицию головы в начале истории
        self.history.insert(0, (self.x, self.y))

        # Обрезаем историю, чтобы не копить память
        max_hist = (self.length + 2) * SEGMENT_SPACING
        if len(self.history) > max_hist:
            del self.history[max_hist:]

        # Столкновение со стеной окна — смерть
        if (self.x < 0 or self.x > WINDOW_WIDTH or
                self.y < 0 or self.y > WINDOW_HEIGHT):
            self.alive = False

    def get_segments(self):
        # Позиции сегментов хвоста (без головы)
        segments = []
        for i in range(1, self.length + 1):
            idx = i * SEGMENT_SPACING
            if idx < len(self.history):
                segments.append(self.history[idx])
        return segments

    def grow(self):
        # Увеличение длины при съедании еды
        self.length += 1

    def check_self_collision(self):
        # Столкновение головы с собственным телом
        for sx, sy in self.get_segments():
            dx = self.x - sx
            dy = self.y - sy
            # Считаем удар, если сегмент ближе чем 0.8 радиуса головы
            if dx * dx + dy * dy < (SNAKE_HEAD_RADIUS * 0.8) ** 2:
                self.alive = False
                return True
        return False

    def draw(self, surface: pygame.Surface):
        # Отрисовка тела и головы
        # Тело — от яркого к тёмному
        segments = self.get_segments()
        n = max(1, len(segments))
        for i, (sx, sy) in enumerate(segments):
            t = i / n
            color = self._lerp(COLORS["snake_body"], (20, 60, 40), t)
            pygame.draw.circle(surface, color,
                               (int(sx), int(sy)),
                               SNAKE_SEGMENT_RADIUS)

        # Голова + светящийся контур
        pygame.draw.circle(surface, COLORS["snake_head"],
                           (int(self.x), int(self.y)),
                           SNAKE_HEAD_RADIUS)
        pygame.draw.circle(surface, COLORS["snake_glow"],
                           (int(self.x), int(self.y)),
                           SNAKE_HEAD_RADIUS, 2)

    @staticmethod
    def _lerp(c1, c2, t):
        # Линейная интерполяция между двумя цветами
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )