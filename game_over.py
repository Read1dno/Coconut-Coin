import pygame
import sys
import json
import os
import math

# Инициализация Pygame
pygame.init()

# Установка окна на полный экран
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Game Over Screen')

# Получение размеров экрана
screen_width, screen_height = screen.get_size()

# Загрузка ресурсов
background = pygame.image.load('sprits/game_over/game_over.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

font_path = 'fonts/HomeVideo-Regular.otf'
font_size = 55
font_color = (255, 255, 255)  # Белый цвет

menu_img = pygame.image.load('sprits/game_over/menu.png')
menu_hover_img = pygame.image.load('sprits/game_over/menuactive.png')

font = pygame.font.Font(font_path, font_size)

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def get_settings_file_path(difficulty):
    return f'settings/top/top_{difficulty}.json'

def load_game_data():
    file_path = 'settings/top/game_over.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data.get('max_score', 0), data.get('game_duration', 0)
    return 0, 0

def load_game_over_data():
    config = load_config()
    difficulty = config['difficulty']
    settings_file_path = get_settings_file_path(difficulty)
    if os.path.exists(settings_file_path):
        with open(settings_file_path, 'r') as f:
            data = json.load(f)
        return data.get('max_score', 0), data.get('formatted_time', "00:00:00")
    return 0, "00:00:00"

def save_game_over_data(max_score, formatted_time):
    config = load_config()
    difficulty = config['difficulty']
    settings_file_path = get_settings_file_path(difficulty)
    data = {
        'max_score': max_score,
        'formatted_time': formatted_time
    }
    os.makedirs(os.path.dirname(settings_file_path), exist_ok=True)
    with open(settings_file_path, 'w') as f:
        json.dump(data, f)

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'

def game_over_screen():
    # Загрузка текущих данных из файла game_over.json и вызов экрана
    current_score, game_duration = load_game_data()
    max_score, saved_time = load_game_over_data()
    new_record = current_score > max_score

    if new_record:
        max_score = current_score
        formatted_time = format_time(game_duration)
        save_game_over_data(max_score, formatted_time)

    running = True
    start_ticks = pygame.time.get_ticks()
    period = 1000  # период в миллисекундах для одного цикла анимации
    start_size = 65
    end_size = 75

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Переход в меню

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                menu_rect = menu_img.get_rect(center=(screen_width // 2, screen_height // 2 + 250))
                if menu_rect.collidepoint(mouse_pos):
                    return "game_over"

        screen.blit(background, (0, 0))

        formatted_time = format_time(game_duration)

        max_score_text = font.render(f'Счет: {max_score}', True, font_color)
        game_time_text = font.render(f'Время игры: {formatted_time}', True, font_color)

        max_score_rect = max_score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        game_time_rect = game_time_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

        screen.blit(max_score_text, max_score_rect)
        screen.blit(game_time_text, game_time_rect)

        if new_record:
            ticks = pygame.time.get_ticks()
            elapsed_time = ticks - start_ticks
            # Использование синусоидальной функции для плавной анимации
            scale = (math.sin(2 * math.pi * (elapsed_time % period) / period) + 1) / 2
            current_size = start_size + (end_size - start_size) * scale
            anim_font = pygame.font.Font(font_path, int(current_size))
            new_record_text = anim_font.render("Новый рекорд!", True, font_color)
            new_record_rect = new_record_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
            screen.blit(new_record_text, new_record_rect)

        menu_rect = menu_img.get_rect(center=(screen_width // 2, screen_height // 2 + 250))

        mouse_pos = pygame.mouse.get_pos()

        if menu_rect.collidepoint(mouse_pos):
            screen.blit(menu_hover_img, menu_rect)
        else:
            screen.blit(menu_img, menu_rect)

        pygame.display.flip()
