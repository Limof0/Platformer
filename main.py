import pygame
import sys
from game import Game


def main():
    pygame.init()

    # Настройки окна
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Платформер 'Прыгун'")

    # Создание игры
    game = Game(screen)

    # Основной игровой цикл
    clock = pygame.time.Clock()
    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset_level()
                elif event.key == pygame.K_n and game.level_complete:
                    game.next_level()
                elif event.key == pygame.K_p:
                    game.paused = not game.paused

        # Обновление игры
        if not game.paused:
            game.update()

        # Отрисовка
        game.draw()

         # Показ итоговой статистики при завершении игры
        if game.current_level == 9 and game.level_complete:
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            title_font = pygame.font.SysFont(None, 48)
            stats_font = pygame.font.SysFont(None, 36)

            # Заголовок
            title = title_font.render("ИГРА ПРОЙДЕНА!", True, (255, 255, 100))
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

            # Статистика по монетам
            coins_collected = game.coins_collected
            total_coins = game.total_coins

            if coins_collected == total_coins:
                coins_text = stats_font.render(f"Вы собрали ВСЕ {total_coins} монет! Отлично!", True, (255, 215, 0))
            else:
                coins_text = stats_font.render(f"Вы собрали {coins_collected} из {total_coins} монет", True,
                                               (255, 255, 200))

            screen.blit(coins_text, (screen.get_width() // 2 - coins_text.get_width() // 2, 200))

            # Инструкция
            instruction = stats_font.render("Нажмите ESC для выхода", True, (200, 200, 255))
            screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, 300))
        
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    main()

