# Класс Game: игровой цикл, состояния, отрисовка меню / HUD / Game Over
import sys
import random
import math
import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    STATE_MENU, STATE_PLAY, STATE_GAME_OVER,
    MAGNET_RADIUS, FOOD_SPAWN_MARGIN, SCORE_PER_FOOD,
    COLORS,
)
from snake import Snake
from food import Food


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Magnetic Snake — ЛР 1 (вариант 13)")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 24)
        self.mid_font = pygame.font.Font(None, 40)
        self.big_font = pygame.font.Font(None, 64)

        self.state = STATE_MENU
        self.score = 0
        self.best_score = 0

        self.snake = None
        self.food = None

    # ЛОГИКА СОСТОЯНИЙ
    def start_game(self):
        self.snake = Snake(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.food = self._spawn_food()
        self.score = 0
        self.state = STATE_PLAY

    def _spawn_food(self):
        margin = FOOD_SPAWN_MARGIN
        for _ in range(100):
            x = random.randint(margin, WINDOW_WIDTH - margin)
            y = random.randint(margin, WINDOW_HEIGHT - margin)
            if math.hypot(x - self.snake.x, y - self.snake.y) > 100:
                return Food(x, y)
        return Food(WINDOW_WIDTH // 2, 100)

    # СОБЫТИЯ
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self._quit()

                elif self.state == STATE_GAME_OVER:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

    def handle_continuous_input(self):
        """Обработка зажатых A/D — поворот змейки."""
        if self.state != STATE_PLAY or not self.snake.alive:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.snake.turn(-1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.snake.turn(+1)

    # ОБНОВЛЕНИЕ
    def update(self):
        if self.state != STATE_PLAY:
            return

        self.snake.update()
        self.food.update(self.snake)

        # Съедание
        if self.food.check_eaten(self.snake):
            self.score += SCORE_PER_FOOD
            self.snake.grow()
            self.food = self._spawn_food()

        # Столкновение с хвостом
        self.snake.check_self_collision()

        # Проверка проигрыша
        if not self.snake.alive:
            self.best_score = max(self.best_score, self.score)
            self.state = STATE_GAME_OVER

    # ОТРИСОВКА
    def draw(self):
        self.screen.fill(COLORS["bg"])
        self._draw_grid()

        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PLAY:
            self._draw_play()
        elif self.state == STATE_GAME_OVER:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_grid(self):
        for x in range(0, WINDOW_WIDTH, 40):
            pygame.draw.line(self.screen, COLORS["grid"], (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.line(self.screen, COLORS["grid"], (0, y), (WINDOW_WIDTH, y))

    def _draw_magnet_field(self):
        """Круг радиуса магнетизма вокруг головы (визуальная подсказка)."""
        if not (self.snake and self.snake.alive):
            return
        pulse = int(6 * (1 + math.sin(pygame.time.get_ticks() * 0.005)))
        r = MAGNET_RADIUS + pulse
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*COLORS["magnet_field"], 30),
                           (r, r), r, 2)
        self.screen.blit(surf, (self.snake.x - r, self.snake.y - r))

    def _draw_play(self):
        self._draw_magnet_field()
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        self._draw_hud()

    def _draw_hud(self):
        score_s = self.font.render(f"Очки: {self.score}", True, COLORS["text"])
        self.screen.blit(score_s, (15, 12))

        len_s = self.font.render(f"Длина: {self.snake.length}",
                                 True, COLORS["text_dim"])
        self.screen.blit(len_s, (15, 38))

        hint = self.font.render("A / D — поворот    ESC — выход",
                                True, COLORS["text_dim"])
        rect = hint.get_rect()
        rect.topright = (WINDOW_WIDTH - 15, 12)
        self.screen.blit(hint, rect)

    def _draw_menu(self):
        t = self.big_font.render("MAGNETIC SNAKE", True, COLORS["snake_glow"])
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 160)))

        st = self.mid_font.render("Змейка-Магнит", True, COLORS["accent"])
        self.screen.blit(st, st.get_rect(center=(WINDOW_WIDTH // 2, 220)))

        lines = [
            "Управление:  A / D — поворот",
            "Еда притягивается к змейке ближе 150 px (магнетизм)",
            "Собирай еду, расти и не врезайся в стены и себя!",
            "",
            "ENTER / SPACE — начать игру",
            "ESC — выход",
        ]
        for i, line in enumerate(lines):
            s = self.font.render(line, True, COLORS["text"])
            self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 28)))

    def _draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        t = self.big_font.render("ИГРА ОКОНЧЕНА", True, COLORS["game_over"])
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 210)))

        s = self.mid_font.render(f"Очки: {self.score}", True, COLORS["text"])
        self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, 290)))

        b = self.font.render(f"Лучший результат: {self.best_score}",
                             True, COLORS["text_dim"])
        self.screen.blit(b, b.get_rect(center=(WINDOW_WIDTH // 2, 340)))

        h = self.font.render("ENTER — сыграть заново    ESC — в меню",
                             True, COLORS["text"])
        self.screen.blit(h, h.get_rect(center=(WINDOW_WIDTH // 2, 420)))

    # СЛУЖЕБНОЕ
    def _quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.handle_continuous_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)