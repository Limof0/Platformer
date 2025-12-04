# Структура уровня:
# {
#     "player_start": (x, y),
#     "goal": (x, y),
#     "platforms": [(x, y, width, height, type, move_range), ...],
#     "enemies": [(x, y, patrol_range), ...]
# }

levels = [
  # Уровень 1 - Начало, обучение
    {
        "player_start": (100, 500), # Точка спавна
        "goal": (900, 300), # Финиш
        "platforms": [
            (0, 600, 1000, 100, "normal", 0),  # Земля
            (200, 500, 200, 30, "normal", 0),  # Обычная платформа
            (500, 450, 200, 30, "normal", 0),
            (800, 400, 200, 30, "normal", 0),
        ],
        "enemies": []
    },
