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
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    main()
