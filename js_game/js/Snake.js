import { CONSTANTS } from './constants.js';
import { distance } from './math_utils.js';

// Конечный автомат (Состояния змейки)
export const SNAKE_STATE = Object.freeze({
    MOVING: 'MOVING',
    EATING: 'EATING',
    DEAD: 'DEAD'
});

export class Snake {
    constructor(x, y, speed) {
        this.x = x;
        this.y = y;
        this.angle = 0;
        this.speed = speed || CONSTANTS.SNAKE_SPEED;
        this.length = CONSTANTS.SNAKE_START_LENGTH;
        this.state = SNAKE_STATE.MOVING; // Текущее состояние (FSM)
        this.history = [[this.x, this.y]];
    }

    turn(direction) {
        this.angle = (this.angle + direction * CONSTANTS.SNAKE_TURN_SPEED) % 360;
    }

    update() {
        if (this.state === SNAKE_STATE.DEAD) return;

        const rad = this.angle * Math.PI / 180;
        this.x += this.speed * Math.cos(rad);
        this.y += this.speed * Math.sin(rad);

        this.history.unshift([this.x, this.y]);
        const maxHist = (this.length + 2) * CONSTANTS.SEGMENT_SPACING;
        if (this.history.length > maxHist) this.history.length = maxHist;

        if (this.x < 0 || this.x > CONSTANTS.WINDOW_WIDTH ||
            this.y < 0 || this.y > CONSTANTS.WINDOW_HEIGHT) {
            this.state = SNAKE_STATE.DEAD; // Переход состояния
        }
    }

    // НОВОЕ: Вычисление угла между змейкой и едой (по ТЗ варианта 13)
    getAngleTo(targetX, targetY) {
        const dx = targetX - this.x;
        const dy = targetY - this.y;
        // Math.atan2 возвращает угол в радианах от -Pi до Pi
        // Переводит в градусы
        return Math.atan2(dy, dx) * 180 / Math.PI;
    }

    getSegments() {
        const segments = [];
        for (let i = 1; i <= this.length; i++) {
            const idx = i * CONSTANTS.SEGMENT_SPACING;
            if (idx < this.history.length) segments.push(this.history[idx]);
        }
        return segments;
    }

    grow() {
        this.length += 1;
        this.state = SNAKE_STATE.EATING;
        // Через кадр вернется в движение
        setTimeout(() => { if (this.state !== SNAKE_STATE.DEAD) this.state = SNAKE_STATE.MOVING; }, 100);
    }

    checkSelfCollision() {
        const segments = this.getSegments();
        for (const [sx, sy] of segments) {
            if (distance(this.x, this.y, sx, sy) < CONSTANTS.SNAKE_SPEED * 0.8) {
                this.state = SNAKE_STATE.DEAD;
                return;
            }
        }
    }
}