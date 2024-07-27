import pygame
import json
import os

def settings_screen():
    # Инициализация PyGame
    pygame.init()
    
    # Загрузка конфигурации
    config_path = "config.json"
    if not os.path.exists(config_path):
        config = {"difficulty": 1, "fullscreen": "yes", "sound": 50}
    else:
        with open(config_path, "r") as f:
            config = json.load(f)

    # Настройки экрана (весь экран)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Настройки игры")

    # Загрузка изображений
    bg_image = pygame.image.load("sprits/settings/settings.png")
    cube_image = pygame.image.load("sprits/settings/cube.png")
    cube_full_image = pygame.image.load("sprits/settings/cube_full.png")
    polzunok_image = pygame.image.load("sprits/settings/polzunok.png")

    # Загрузка шрифта
    font = pygame.font.Font("fonts/HomeVideo-Regular.otf", 35)

    # Параметры клеточек
    cube_width, cube_height = cube_image.get_size()
    cube_full_width, cube_full_height = cube_full_image.get_size()

    # Параметры ползунка
    polzunok_width, polzunok_height = polzunok_image.get_size()
    sound_bar_x, sound_bar_y = 540, 712  # Позиция полоски звука
    sound_bar_width = 360  # Длина полоски звука

    # Установка начальной позиции ползунка в зависимости от значения в конфиге
    polzunok_x = sound_bar_x + (sound_bar_width - polzunok_width) * (config["sound"] / 100)
    polzunok_y = sound_bar_y - (polzunok_height // 2)

    # Позиции клеточек (эти переменные можно настроить вручную)
    difficulty_start_x, difficulty_start_y = 1040, 450  # Начальная позиция клеточек сложности
    fullscreen_start_x, fullscreen_start_y = 565, 475  # Начальная позиция клеточек режима экрана

    difficulty_spacing = 23  # Отступы между клеточками сложности
    fullscreen_spacing = 20  # Отступы между клеточками режима экрана

    # Позиции клеточек сложности
    difficulty_cubes = [
        (difficulty_start_x, difficulty_start_y + i * (cube_height + difficulty_spacing)) for i in range(5)
    ]
    # Позиции клеточек режима экрана
    fullscreen_cubes = [
        (fullscreen_start_x, fullscreen_start_y + i * (cube_full_height + fullscreen_spacing)) for i in range(2)
    ]

    # Функция для рисования крестиков
    def draw_x(screen, position):
        text = font.render("X", True, (0, 0, 0))
        screen.blit(text, (position[0] + (cube_width - text.get_width()) // 2,
                           position[1] + (cube_height - text.get_height()) // 2))

    # Основной цикл
    running = True
    dragging = False
    while running:
        screen.blit(bg_image, (0, 0))

        # Рисование клеточек сложности
        for idx, pos in enumerate(difficulty_cubes):
            screen.blit(cube_image, pos)
            if config["difficulty"] == 5 - idx:  # Инвертируем порядок сложности
                draw_x(screen, pos)

        # Рисование клеточек режима экрана
        for idx, pos in enumerate(fullscreen_cubes):
            screen.blit(cube_full_image, pos)
            if (config["fullscreen"] == "yes" and idx == 0) or (config["fullscreen"] == "no" and idx == 1):
                draw_x(screen, pos)

        # Рисование ползунка
        screen.blit(polzunok_image, (polzunok_x, polzunok_y))

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "settings"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    with open(config_path, "w") as f:
                        json.dump(config, f)
                    return "settings"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for idx, pos in enumerate(difficulty_cubes):
                    rect = pygame.Rect(pos[0], pos[1], cube_width, cube_height)
                    if rect.collidepoint(mouse_pos):
                        config["difficulty"] = 5 - idx  # Инвертируем порядок сложности

                for idx, pos in enumerate(fullscreen_cubes):
                    rect = pygame.Rect(pos[0], pos[1], cube_full_width, cube_full_height)
                    if rect.collidepoint(mouse_pos):
                        config["fullscreen"] = "yes" if idx == 0 else "no"

                # Проверка нажатия на ползунок
                polzunok_rect = pygame.Rect(polzunok_x, polzunok_y, polzunok_width, polzunok_height)
                if polzunok_rect.collidepoint(mouse_pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x = event.pos[0]
                    # Обновление позиции ползунка и значения звука
                    polzunok_x = max(sound_bar_x, min(mouse_x - polzunok_width // 2, sound_bar_x + sound_bar_width - polzunok_width))
                    config["sound"] = int((polzunok_x - sound_bar_x) / (sound_bar_width - polzunok_width) * 100)