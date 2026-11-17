export function createScenarios(widget) {
    return {
        // Ускоряет змейку в 2 раза
        speedUp() {
            widget.game.snake.speed *= 2;
            console.log("Сценарий: Змейка ускорена!");
        },
        // Включает/выключает туман войны (ограниченную видимость)
        toggleFog() {
            widget.fogEnabled = !widget.fogEnabled;
            console.log(`Туман войны: ${widget.fogEnabled ? 'ВКЛ' : 'ВЫКЛ'}`);
        },
        // Телепортирует еду в случайное место (эмулирует спавн)
        addFood() {
            widget.game.food = widget.game.spawnFood();
            console.log("Сценарий: Еда перемещена!");
        },
        // Полный перезапуск игры
        reset() {
            widget.initGame();
            console.log("Сценарий: Игра сброшена!");
        }
    };
}