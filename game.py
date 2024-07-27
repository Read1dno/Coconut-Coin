import pygame
import time
import random
import sys
import json
import os

# Инициализация Pygame
pygame.init()

# Загрузка и масштабирование изображений
def load_and_scale_image(path, scale_factor=1):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale_factor, image.get_height() // scale_factor))

background_image = load_and_scale_image("sprits/game/fon.png", 1)

# Загрузка кадров анимации бомбы
bomb_frames = [load_and_scale_image(f"sprits/game/bomb/bomb-{i}.png", 2) for i in range(7)]
coin_image = load_and_scale_image("sprits/game/coin.png", 2)

# Загрузка шрифта
font = pygame.font.Font("fonts/HomeVideo-Regular.otf", 36)

# Цвета
WHITE = (255, 255, 255)

def generate_fall_speeds(fall_speed):
    """ Генерирует три скорости падения на основе текущей fall_speed """
    min_speed = fall_speed * 0.8  # 20% меньше
    max_speed = fall_speed * 1.6  # 60% больше
    return [
        min_speed + (max_speed - min_speed) * 0.2,  # 20% от диапазона
        min_speed + (max_speed - min_speed) * 0.5,  # 50% от диапазона
        min_speed + (max_speed - min_speed) * 0.8   # 80% от диапазона
    ]

def spawn_item(image_frames, spawn_rate, items_list, screen_width, fall_speed):
    if random.random() < spawn_rate:
        x = random.randint(0, screen_width - image_frames[0].get_width())
        y = -image_frames[0].get_height()
        fall_speeds = generate_fall_speeds(fall_speed)  # Генерация скоростей
        speed = random.choice(fall_speeds)  # Выбор случайной скорости
        items_list.append({
            'rect': pygame.Rect(x, y, image_frames[0].get_width(), image_frames[0].get_height()),
            'frames': image_frames,
            'frame_index': 0,
            'speed': speed,
            'last_update': pygame.time.get_ticks()
        })

def update_items(items_list, screen_height, item_type, score, lives):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    to_remove = []

    for item in items_list:
        item['rect'].y += item['speed']  # Используем случайную скорость

        # Обновление текущего кадра анимации
        current_time = pygame.time.get_ticks()
        if current_time - item['last_update'] > 300:  # смена кадра каждые 300 мс
            if item['frame_index'] < len(item['frames']) - 1:
                item['frame_index'] += 1
            item['last_update'] = current_time

        if item['rect'].y > screen_height:
            to_remove.append(item)
            if item_type == 'coin':
                lives -= 1
                if lives <= 0:
                    return 'game_over', score, lives
        
        elif mouse_pressed and item['rect'].collidepoint(mouse_x, mouse_y):
            to_remove.append(item)
            if item_type == 'coin':
                score += 5
            elif item_type == 'bomb':
                score -= 50
                if score < 0:
                    score = 0
                    lives -= 1
                    if lives <= 0:
                        return 'game_over', score, lives
    
    for item in to_remove:
        items_list.remove(item)

    return None, score, lives

def draw_items(items_list, screen):
    for item in items_list:
        frame = item['frames'][item['frame_index']]
        screen.blit(frame, item['rect'].topleft)

def draw_text(screen, text, font, color, position):
    surface = font.render(text, True, color)
    screen.blit(surface, position)

def save_game_over_data(score, elapsed_time):
    # Создание папки, если она не существует
    os.makedirs('settings/top', exist_ok=True)

    # Данные для сохранения
    data = {
        'max_score': score,
        'game_duration': int(elapsed_time)  # Преобразование времени в целое число
    }

    # Запись данных в файл
    with open('settings/top/game_over.json', 'w') as f:
        json.dump(data, f, indent=4)

def game(screen_width, screen_height, initial_score, initial_lives, fall_speed, bomb_spawn_rate, coin_spawn_rate):
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN if screen_height == pygame.display.Info().current_h else 0)
    clock = pygame.time.Clock()

    score = initial_score
    lives = initial_lives
    bombs = []
    coins = []
    
    running = True
    start_time = pygame.time.get_ticks()
    last_speed_increase_time = start_time  # Время последнего увеличения скорости

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        spawn_item(bomb_frames, bomb_spawn_rate, bombs, screen_width, fall_speed)
        spawn_item([coin_image], coin_spawn_rate, coins, screen_width, fall_speed)
        
        result, score, lives = update_items(bombs, screen_height, 'bomb', score, lives)
        if result == 'game_over':
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            save_game_over_data(score, elapsed_time)
            return 'game_over'

        result, score, lives = update_items(coins, screen_height, 'coin', score, lives)
        if result == 'game_over':
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            save_game_over_data(score, elapsed_time)
            return 'game_over'
        
        current_time = pygame.time.get_ticks() / 1000
        elapsed_time = current_time - (start_time / 1000)

        # Обновление скорости падения каждые 60 секунд
        if current_time - (last_speed_increase_time / 1000) > 60:
            fall_speed += 1
            last_speed_increase_time = pygame.time.get_ticks()  # Обновление времени последнего увеличения скорости

        screen.blit(background_image, (0, 0))
        draw_items(bombs, screen)
        draw_items(coins, screen)
        
        draw_text(screen, f"Счет: {score}", font, WHITE, (10, 10))
        draw_text(screen, f"Жизни: {lives}", font, WHITE, (10, 50))
        
        pygame.display.flip()
        time.sleep(0.01)

    return 'quit'
