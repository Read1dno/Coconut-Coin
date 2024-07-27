import json
import pygame
import os

def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        return {"difficulty": 1, "fullscreen": "yes", "sound": 50}
    else:
        with open(config_path, "r") as f:
            return json.load(f)

def get_screen_size():
    config = load_config()
    if config["fullscreen"] == "yes":
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        width, height = screen.get_size()
    else:
        screen = pygame.display.set_mode((0, 0))
        width, height = screen.get_size()
        height -= 40
    return width, height

def get_game_parameters():
    config = load_config()
    difficulty = config.get("difficulty", 1)
    
    if difficulty == 1:  # Легкий уровень
        score = 200
        lives = 5
        fall_speed = 2
        bomb_spawn_rate = 0.005
        coin_spawn_rate = 0.05
    elif difficulty == 2:  # Средний уровень
        score = 100
        lives = 5
        fall_speed = 3
        bomb_spawn_rate = 0.01
        coin_spawn_rate = 0.1
    elif difficulty == 3:  # Сложный уровень
        score = 100
        lives = 3
        fall_speed = 4
        bomb_spawn_rate = 0.01
        coin_spawn_rate = 0.1
    elif difficulty == 4:  # Очень сложный уровень
        score = 100
        lives = 2
        fall_speed = 5
        bomb_spawn_rate = 0.02
        coin_spawn_rate = 0.2
    elif difficulty == 5:  # Экстремальный уровень
        score = 0
        lives = 1
        fall_speed = 6
        bomb_spawn_rate = 0.02
        coin_spawn_rate = 0.2
    else:  # Значение по умолчанию для неопределенного уровня сложности
        score = 100
        lives = 3
        fall_speed = 3
        bomb_spawn_rate = 0.01
        coin_spawn_rate = 0.1
    
    return score, lives, fall_speed, bomb_spawn_rate, coin_spawn_rate

def get_sound_level():
    config = load_config()
    return config.get("sound", 50)

# Пример использования функций
if __name__ == "__main__":
    pygame.init()
    width, height = get_screen_size()
    print(f"Screen size: {width}x{height}")

    score, lives, fall_speed, bomb_spawn_rate, coin_spawn_rate = get_game_parameters()
    print(f"Score: {score}, Lives: {lives}, Fall Speed: {fall_speed}, Bomb Spawn Rate: {bomb_spawn_rate}, Coin Spawn Rate: {coin_spawn_rate}")

    sound_level = get_sound_level()
    print(f"Sound level: {sound_level}")
    pygame.quit()
