import pygame
import game
import game_over
import settings
import config
import results
import sys

# Инициализация Pygame
pygame.init()

# Инициализация микшера Pygame
pygame.mixer.init()

# Загрузка музыки
pygame.mixer.music.load('sound/Bloom-Colorful_Cat.mp3')

# Получение уровня громкости из config.py
sound_level = config.get_sound_level() / 100.0
pygame.mixer.music.set_volume(sound_level)  # Установка громкости

# Запуск воспроизведения музыки на повторе
pygame.mixer.music.play(-1)

# Получение размеров экрана из config.py
width, height = config.get_screen_size()

# Определение размеров экрана и создание окна
if height == pygame.display.Info().current_h - 40:
    screen = pygame.display.set_mode((width, height))
else:
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Цвет фона
BACKGROUND_COLOR = (0, 0, 0)

# Загрузка изображений
background_img = pygame.image.load('sprits/menu/menu.png')
background_img = pygame.transform.scale(background_img, (width, height))

play_btn = pygame.image.load('sprits/menu/play.png')
settings_btn = pygame.image.load('sprits/menu/settings.png')
top_btn = pygame.image.load('sprits/menu/top.png')
exit_btn = pygame.image.load('sprits/menu/exit.png')

play_btn_active = pygame.image.load('sprits/menu/playactive.png')
settings_btn_active = pygame.image.load('sprits/menu/settingsactive.png')
top_btn_active = pygame.image.load('sprits/menu/topactive.png')
exit_btn_active = pygame.image.load('sprits/menu/exitactive.png')

# Размеры и отступы кнопок
button_margin = 13
button_size = play_btn.get_width(), play_btn.get_height()

# Вычисление центра экрана и размещение кнопок
total_button_height = (button_size[1] * 4) + (button_margin * 3)
start_y = (height - total_button_height) // 2

def draw_buttons(screen, active_button):
    y = start_y
    screen.blit(play_btn_active if active_button == 'play' else play_btn, ((width - button_size[0]) // 2, y))
    y += button_size[1] + button_margin
    screen.blit(settings_btn_active if active_button == 'settings' else settings_btn, ((width - button_size[0]) // 2, y))
    y += button_size[1] + button_margin
    screen.blit(top_btn_active if active_button == 'top' else top_btn, ((width - button_size[0]) // 2, y))
    y += button_size[1] + button_margin
    screen.blit(exit_btn_active if active_button == 'exit' else exit_btn, ((width - button_size[0]) // 2, y))

def get_button_rects():
    rects = []
    y = start_y
    for _ in range(4):
        rects.append(pygame.Rect((width - button_size[0]) // 2, y, button_size[0], button_size[1]))
        y += button_size[1] + button_margin
    return rects

def launch_game():
    screen_width, screen_height = config.get_screen_size()
    score, lives, fall_speed, bomb_spawn_rate, coin_spawn_rate = config.get_game_parameters()
    result = game.game(screen_width, screen_height, score, lives, fall_speed, bomb_spawn_rate, coin_spawn_rate)
    return result

def check_and_update_volume():
    global sound_level
    new_sound_level = config.get_sound_level() / 100.0
    if new_sound_level != sound_level:
        sound_level = new_sound_level
        pygame.mixer.music.set_volume(sound_level)

def main():
    running = True
    active_button = None

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rects = get_button_rects()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_rects[0].collidepoint(x, y):
                    result = launch_game()
                    if result == 'game_over':
                        gameover = game_over.game_over_screen()
                        if gameover == "game_over":
                            continue
                        continue  # Возвращаемся в меню
                    running = False
                elif button_rects[1].collidepoint(x, y):
                    result = settings.settings_screen()
                    if result == "settings":
                        continue
                elif button_rects[2].collidepoint(x, y):
                    result = results.show_results()
                    if result == "exit":
                        continue
                elif button_rects[3].collidepoint(x, y):
                    running = False

        # Определение активной кнопки и изменение курсора
        new_active_button = None
        cursor_type = pygame.SYSTEM_CURSOR_ARROW  # Стандартный курсор по умолчанию

        for i, rect in enumerate(button_rects):
            if rect.collidepoint(mouse_x, mouse_y):
                new_active_button = ['play', 'settings', 'top', 'exit'][i]
                cursor_type = pygame.SYSTEM_CURSOR_HAND  # Курсор указателя
                break

        if new_active_button != active_button:
            active_button = new_active_button

        pygame.mouse.set_cursor(cursor_type)  # Установка текущего курсора

        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_img, (0, 0))
        draw_buttons(screen, active_button)

        pygame.display.flip()

        # Проверка и обновление громкости
        check_and_update_volume()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
