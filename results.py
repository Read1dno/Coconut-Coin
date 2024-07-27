import pygame
import json
import os

def show_results():
    # Установим размеры экрана
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    
    # Загрузим шрифт
    try:
        font = pygame.font.Font('fonts/HomeVideo-Regular.otf', 55)
    except FileNotFoundError:
        print("Шрифт не найден. Пожалуйста, убедитесь, что файл 'HomeVideo-Regular.otf' находится в папке 'fonts'.")
        return "exit"

    # Индекс текущего уровня сложности
    difficulty_index = 3  # Начнем с уровня "Нормально"
    
    # Загрузим изображение
    try:
        results_bg = pygame.image.load('sprits/results/results.png')
    except pygame.error as e:
        print(f"Ошибка загрузки изображения: {e}")
        return "exit"
    
    def load_results(difficulty_index):
        """Загрузить результаты из файла."""
        file_path = f'settings/top/top_{difficulty_index}.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data.get('max_score', 0), data.get('formatted_time', '00:00:00')
        return 0, '00:00:00'

    # Определение зон для кнопок
    def is_within_rect(pos, rect):
        return rect.collidepoint(pos)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit"
                elif event.key == pygame.K_RIGHT:
                    if difficulty_index < 5:
                        difficulty_index += 1
                elif event.key == pygame.K_LEFT:
                    if difficulty_index > 1:
                        difficulty_index -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_within_rect(mouse_pos, next_button_rect):
                    if difficulty_index < 5:
                        difficulty_index += 1
                elif is_within_rect(mouse_pos, prev_button_rect):
                    if difficulty_index > 1:
                        difficulty_index -= 1
        
        # Загрузить текущие результаты
        score, formatted_time = load_results(difficulty_index)
        
        # Отобразить фон
        screen.blit(results_bg, (0, 0))
        
        # Подготовка текста
        difficulty_text = 'Практика' if difficulty_index == 1 else \
                          'Легко' if difficulty_index == 2 else \
                          'Нормально' if difficulty_index == 3 else \
                          'Тяжело' if difficulty_index == 4 else \
                          'Сложно'
        score_text = f"Счет: {score}"
        time_text = f"Время игры: {formatted_time}"

        # Рендеринг текста
        difficulty_surf = font.render(difficulty_text, True, (255, 255, 255))
        score_surf = font.render(score_text, True, (255, 255, 255))
        time_surf = font.render(time_text, True, (255, 255, 255))

        # Определение позиций текста
        difficulty_rect = difficulty_surf.get_rect(center=(width // 2, height // 2 - 100))
        score_rect = score_surf.get_rect(center=(width // 2, height // 2 + 10))
        time_rect = time_surf.get_rect(center=(width // 2, height // 2 + 120))

        # Отображение текста
        screen.blit(difficulty_surf, difficulty_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(time_surf, time_rect)

        # Отображение кнопок
        next_button_surf = font.render('>', True, (255, 255, 255))
        next_button_rect = next_button_surf.get_rect(center=(width // 2 + 200, height // 2 - 100))
        screen.blit(next_button_surf, next_button_rect)
        
        prev_button_surf = font.render('<', True, (255, 255, 255))
        prev_button_rect = prev_button_surf.get_rect(center=(width // 2 - 200, height // 2 - 100))
        screen.blit(prev_button_surf, prev_button_rect)

        pygame.display.flip()
        pygame.time.delay(100)  # Задержка для предотвращения излишней загрузки процессора

    return "exit"