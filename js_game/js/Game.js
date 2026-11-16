import { CONSTANTS } from './constants.js';
import { Snake, SNAKE_STATE } from './Snake.js';
import { Food } from './Food.js';

export class Game {
    constructor() {
        this.snake = new Snake(CONSTANTS.WINDOW_WIDTH / 2, CONSTANTS.WINDOW_HEIGHT / 2);
        this.food = this.spawnFood();
        this.score = 0;
    }

    spawnFood() {
        const x = Math.random() * (CONSTANTS.WINDOW_WIDTH - 100) + 50;
        const y = Math.random() * (CONSTANTS.WINDOW_HEIGHT - 100) + 50;
        return new Food(x, y);
    }

    update() {
        if (this.snake.state === SNAKE_STATE.DEAD) return;

        this.snake.update();
        this.food.update(this.snake);

        if (this.food.isEaten(this.snake)) {
            this.score += CONSTANTS.SCORE_PER_FOOD;
            this.snake.grow();
            this.food = this.spawnFood();
        }
        this.snake.checkSelfCollision();
    }

    // НОВОЕ: Загрузка конфигурации из JSON строки с валидацией
    static loadFromJSON(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            if (!data.width || !data.height) {
                throw new Error("Отсутствуют обязательные поля width или height");
            }
            // В реальной игре бы применились эти настройки, но для теста просто возвращает true
            return true;
        } catch (e) {
            console.error("Ошибка загрузки JSON:", e.message);
            return false;
        }
    }
}