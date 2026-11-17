// Импорт ядра из папки ЛР4 (js_game)
import { Game } from '../../js_game/js/Game.js';
import { CONSTANTS } from '../../js_game/js/constants.js';
import { SNAKE_STATE } from '../../js_game/js/Snake.js';
import { createScenarios } from './scenarios.js';

class SnakeWidget {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');

        this.fogEnabled = true;
        this.keys = {}; // Массив-флаги для клавиш
        this.mouse = { x: 0, y: 0, active: false }; // Для управления мышью
        this.accumulator = 0;
        this.FRAME_MS = 1000 / 60; // Фиксированный шаг симуляции (16.6 мс)
        this.lastTime = performance.now();

        this.initGame();
        this.setupInput();

        // Создает сценарии и выставляет их глобально для консоли
        this.scenarios = createScenarios(this);
        window.SnakeWidget = this;

        this.setupButtons();

        // Запуск игрового цикла
        requestAnimationFrame((time) => this.loop(time));
    }

    initGame() {
        this.game = new Game();
        this.keys = {}; // Очищает зажатые клавиши
        this.mouse.active = false; // Сбрасывает мышь
        this.updateHUD();
    }

    setupInput() {
        // Оставляет клавиши на всякий случай, но основное - мышь
        window.addEventListener('keydown', (e) => {
            this.keys[e.key.toLowerCase()] = true;
        });
        window.addEventListener('keyup', (e) => {
            this.keys[e.key.toLowerCase()] = false;
        });

        // Отслеживаем мышку на холсте
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
            this.mouse.active = true;
        });
    }

    setupButtons() {
        // Привязываем кнопки из HTML к сценариям
        document.querySelectorAll('[data-scenario]').forEach(btn => {
            btn.addEventListener('click', () => {
                const scenarioName = btn.dataset.scenario;
                this.scenarios[scenarioName]();
            });
        });
    }

    updateHUD() {
        // Обновляем DOM-элементы, не пересоздавая их
        document.getElementById('score').textContent = this.game.score;
        document.getElementById('length').textContent = this.game.snake.length;
    }

    loop(now) {
        let deltaMs = Math.min(now - this.lastTime, 100); // Защита от лагов
        this.lastTime = now;
        this.accumulator += deltaMs;

        // Фиксированный шаг симуляции
        while (this.accumulator >= this.FRAME_MS) {
            this.step();
            this.accumulator -= this.FRAME_MS;
        }

        this.draw();
        requestAnimationFrame((time) => this.loop(time));
    }

    step() {
        if (this.game.snake.state === SNAKE_STATE.DEAD) return;

        // УПРАВЛЕНИЕ МЫШЬЮ
        if (this.mouse.active) {
            const snake = this.game.snake;

            // 1. Вычисляет угол от змейки до мыши (использует Math.atan2 из ЛР4)
            const dx = this.mouse.x - snake.x;
            const dy = this.mouse.y - snake.y;
            const targetAngle = Math.atan2(dy, dx) * 180 / Math.PI;

            // 2. Плавно поворачивает змейку к цели
            let diff = targetAngle - snake.angle;

            // Нормализует угол, чтобы змейка не крутилась лишний раз (например, с 350 на 10 градусов)
            while (diff > 180) diff -= 360;
            while (diff < -180) diff += 360;

            // Скорость поворота (берем из констант)
            const turnSpeed = CONSTANTS.SNAKE_TURN_SPEED;

            if (Math.abs(diff) <= turnSpeed) {
                snake.angle = targetAngle; // Если близко, наводит точно
            } else {
                snake.angle += Math.sign(diff) * turnSpeed; // Иначе крутит в нужную сторону
            }
        }

        // Обновляем логику ядра
        this.game.update();
        this.updateHUD();
    }

    draw() {
        // 1. Очищаем экран
        this.ctx.fillStyle = '#9b1818';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.drawGrid();
        this.drawFood(this.game.food);
        this.drawSnake(this.game.snake);
        this.drawMagneticAura(this.game.snake);

        // 2. РЕАЛИЗАЦИЯ ТУМАНА ВОЙНЫ (Маска)
        if (this.fogEnabled) {
            const snake = this.game.snake;
            // Создаем радиальный градиент от змейки
            const gradient = this.ctx.createRadialGradient(
                snake.x, snake.y, 50,   // Внутренний круг (полностью прозрачный)
                snake.x, snake.y, 250   // Внешний круг (непрозрачный черный)
            );
            gradient.addColorStop(0, 'rgba(0, 0, 0, 0)'); // Прозрачный центр
            gradient.addColorStop(1, 'rgba(0, 0, 0, 1)'); // Черные края

            this.ctx.fillStyle = gradient;
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        }

        // 3. Экран Game Over (рисуется поверх всего)
        if (this.game.snake.state === SNAKE_STATE.DEAD) {
            this.drawGameOver();
        }
    }

    drawGrid() {
        this.ctx.strokeStyle = '#1a1a1a';
        this.ctx.lineWidth = 1;
        for (let i = 0; i < this.canvas.width; i += 40) {
            this.ctx.beginPath(); this.ctx.moveTo(i, 0); this.ctx.lineTo(i, this.canvas.height); this.ctx.stroke();
        }
        for (let i = 0; i < this.canvas.height; i += 40) {
            this.ctx.beginPath(); this.ctx.moveTo(0, i); this.ctx.lineTo(this.canvas.width, i); this.ctx.stroke();
        }
    }

    drawSnake(snake) {
        // Рисуем хвост
        const segments = snake.getSegments();
        this.ctx.fillStyle = '#288C46'; // Темно-зеленый
        for (const [sx, sy] of segments) {
            this.ctx.beginPath();
            this.ctx.arc(sx, sy, 8, 0, Math.PI * 2);
            this.ctx.fill();
        }

        // Рисуем голову
        this.ctx.fillStyle = '#50DC78'; // Светло-зеленый
        this.ctx.beginPath();
        this.ctx.arc(snake.x, snake.y, 10, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawFood(food) {
        this.ctx.fillStyle = '#fffd00';
        this.ctx.beginPath();
        this.ctx.arc(food.x, food.y, 8, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawMagneticAura(snake) {
        // Анимация: пульсация радиуса
        const time = performance.now() / 500;
        const pulse = Math.sin(time) * 5;
        const radius = CONSTANTS.MAGNET_RADIUS + pulse;

        // Прозрачность через rgba (альфа-канал)
        this.ctx.strokeStyle = `rgba(0, 255, 77, 0.4)`;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(snake.x, snake.y, radius, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawGameOver() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = '#FF5A5A';
        this.ctx.font = '50px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('ИГРА ОКОНЧЕНА', this.canvas.width / 2, this.canvas.height / 2);

        this.ctx.fillStyle = '#FFF';
        this.ctx.font = '20px Arial';
        this.ctx.fillText('Нажмите "Сбросить игру" в панели справа', this.canvas.width / 2, this.canvas.height / 2 + 50);
    }
}

// Запуск виджета при загрузке страницы
window.addEventListener('DOMContentLoaded', () => {
    new SnakeWidget();
});