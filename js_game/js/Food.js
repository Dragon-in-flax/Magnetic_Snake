import { CONSTANTS } from './constants.js';
import { distance, magnetForce } from './math_utils.js';

export class Food {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        // Случайный угол для дрейфа
        const a = Math.random() * 2 * Math.PI;
        this.vx = Math.cos(a) * CONSTANTS.FOOD_DRIFT_SPEED;
        this.vy = Math.sin(a) * CONSTANTS.FOOD_DRIFT_SPEED;
    }

    update(snake) {
        // 1. Дрейф (свободное движение)
        this.x += this.vx;
        this.y += this.vy;

        // Отскок от стен
        if (this.x < CONSTANTS.FOOD_RADIUS || this.x > CONSTANTS.WINDOW_WIDTH - CONSTANTS.FOOD_RADIUS) {
            this.vx = -this.vx;
        }
        if (this.y < CONSTANTS.FOOD_RADIUS || this.y > CONSTANTS.WINDOW_HEIGHT - CONSTANTS.FOOD_RADIUS) {
            this.vy = -this.vy;
        }

        // 2. Магнетизм (из ЛР2)
        const dist = distance(this.x, this.y, snake.x, snake.y);
        const force = magnetForce(dist, CONSTANTS.MAGNET_RADIUS, CONSTANTS.MAGNET_ACCEL);

        if (force > 0) {
            // Направление от еды к змейке
            const dx = snake.x - this.x;
            const dy = snake.y - this.y;
            const nx = dx / dist;
            const ny = dy / dist;

            // Ускорение еды в сторону змейки
            this.vx += nx * force;
            this.vy += ny * force;

            // Ограничеине максимальной скорости
            const speed = Math.hypot(this.vx, this.vy);
            if (speed > CONSTANTS.MAGNET_MAX_SPEED) {
                this.vx = (this.vx / speed) * CONSTANTS.MAGNET_MAX_SPEED;
                this.vy = (this.vy / speed) * CONSTANTS.MAGNET_MAX_SPEED;
            }
        }
    }

    isEaten(snake) {
        const dist = distance(this.x, this.y, snake.x, snake.y);
        return dist < (CONSTANTS.FOOD_RADIUS + 10); // 10 - радиус головы змейки
    }
}