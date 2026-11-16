// Вычисляет расстояние между двумя точками (теорема Пифагора)
export function distance(x1, y1, x2, y2) {
    return Math.hypot(x2 - x1, y2 - y1);
}

// Вычисляет силу магнетизма. Чем ближе еда, тем сильнее притяжение
export function magnetForce(dist, maxRadius, accel) {
    if (dist >= maxRadius || dist <= 0.001) return 0;
    // Линейное затухание: если dist = 0, сила = accel. Если dist = maxRadius, сила = 0.
    return accel * (1.0 - dist / maxRadius);
}