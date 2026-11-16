import { distance, magnetForce } from './js/math_utils.js';
import { CONSTANTS } from './js/constants.js';
import { Game } from './js/Game.js';
import { Snake, SNAKE_STATE } from './js/Snake.js';

console.log("=== ЗАПУСК САМОПРОВЕРКИ ===");
let passed = 0;
let total = 0;

function assert(condition, message) {
    total++;
    if (condition) { passed++; console.log(`✅ ${message}`); }
    else { console.log(`❌ ОШИБКА: ${message}`); }
}

// --- 1. Геометрия и математика ---
assert(distance(0, 0, 3, 4) === 5, "Теорема Пифагора (3,4 -> 5)");
assert(distance(10, 10, 10, 10) === 0, "Расстояние до себя = 0");
assert(magnetForce(200, 150, 0.6) === 0, "За пределами радиуса силы нет");
assert(magnetForce(0, 150, 0.6) === 0, "В центре (dist=0) нет деления на ноль");
assert(magnetForce(75, 150, 0.6) === 0.3, "В середине радиуса сила равна половине");
assert(magnetForce(100, 150, 0.6).toFixed(2) == (0.6 * (1 - 100 / 150)).toFixed(2), "Проверка линейного затухания");

// --- 2. Логика змейки (FSM и atan2) ---
const snake = new Snake(100, 100, 4.0);
assert(snake.state === SNAKE_STATE.MOVING, "Змейка создается в состоянии MOVING");
assert(snake.x === 100 && snake.y === 100, "Начальные координаты верны");
snake.turn(1); // Поворот вправо
assert(snake.angle === 4.0, "Угол изменился при повороте");
snake.grow();
assert(snake.length === 6, "Длина увеличилась на 1");
assert(snake.state === SNAKE_STATE.EATING, "Состояние изменилось на EATING");

// Проверка Math.atan2 (Вычисление угла)
const angleToFood = snake.getAngleTo(200, 100); // Еда справа
assert(angleToFood === 0, "Угол до еды справа равен 0 градусов");
const angleToTop = snake.getAngleTo(100, 0); // Еда сверху
assert(angleToTop === -90, "Угол до еды сверху равен -90 градусов");
const angleToBottom = snake.getAngleTo(100, 200);
assert(angleToBottom === 90, "Угол до еды снизу равен 90 градусов");

// --- 3. Проверка жизненного цикла ---
snake.x = 850; // Телепортирует за экран
snake.update();
assert(snake.state === SNAKE_STATE.DEAD, "Змейка умирает при выходе за границу");
snake.update(); // Проверка, что мертвая змейка не двигается
assert(snake.state === SNAKE_STATE.DEAD, "Мертвая змейка не меняет состояние");

// --- 4. Игровой цикл и еда ---
const game = new Game();
assert(game.score === 0, "Игра начинается со счета 0");
assert(game.food !== null, "Еда появилась на поле");
// Пододвигает еду к змейке
game.food.x = game.snake.x;
game.food.y = game.snake.y;
game.update();
assert(game.score === 10, "Счет увеличился при съедании еды");
assert(game.snake.length === 6, "Змейка выросла после еды");

// --- 5. Валидация JSON ---
const validJSON = '{"width": 800, "height": 600}';
assert(Game.loadFromJSON(validJSON) === true, "Валидный JSON успешно загружен");
const invalidJSON = '{"width": 800}'; // Нет height
assert(Game.loadFromJSON(invalidJSON) === false, "Невалидный JSON отклонен");
const brokenJSON = '{width: 800'; // Синтаксическая ошибка
assert(Game.loadFromJSON(brokenJSON) === false, "Сломанный JSON отклонен");

console.log(`\n=== РЕЗУЛЬТАТ: ${passed} из ${total} тестов пройдено ===`);