import pygame
import random
from levels import levels


class Player: #Игрок, главный персонаж
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.jump_power = 15
        self.speed = 5
        self.on_ground = False
        self.color = (0, 120, 255)
        self.lives = 3
        self.invincible = 0

        self.direction = 1 # 1 - вправо, -1 - влево

    
    def update(self, platforms, enemies):
        # Гравитация
        self.vel_y += 0.8

        # Ограничение скорости
        self.vel_x = max(-5, min(5, self.vel_x))
        self.vel_y = max(-20, min(20, self.vel_y))

        # Движение по X
        self.x += self.vel_x

        # Проверка коллизий по X
        for platform in platforms:
            if self.check_collision(platform):
                if self.vel_x > 0:
                    self.x = platform.x - self.width
                elif self.vel_x < 0:
                    self.x = platform.x + platform.width
                self.vel_x = 0

        # Движение по Y
        self.y += self.vel_y
        self.on_ground = False

        # Проверка коллизий по Y
        for platform in platforms:
            if self.check_collision(platform):
                if self.vel_y > 0:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                    
    # Обработка столкновений с врагами
        if self.invincible <= 0:
            for enemy in enemies:
                if self.check_collision(enemy):
                    self.lives -= 1
                    self.invincible = 120  # 2 секунда неуязвимости
                    # Отскок от врага
                    self.vel_y = -5
                    if self.x < enemy.x:
                        self.vel_x = -3
                    else:
                        self.vel_x = 3
                    break

        if self.invincible > 0:
            self.invincible -= 1

        # Проверка выхода за границы
        if self.y > 800:
            self.lives -= 1
            self.reset_position()

        # Трение
        self.vel_x *= 0.9

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power

    def move(self, direction):
        self.vel_x += direction * self.speed
        if direction != 0:
            self.direction = direction

    def check_collision(self, obj):
        return (self.x < obj.x + obj.width and
                self.x + self.width > obj.x and
                self.y < obj.y + obj.height and
                self.y + self.height > obj.y)

    def reset_position(self):
        self.x = 100
        self.y = 500
        self.vel_x = 0
        self.vel_y = 0

    def draw(self, screen, camera_x, camera_y):
        # Рисование игрока
        player_rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                                  self.width, self.height)

        # Мерцание при неуязвимости
        if self.invincible <= 0 or self.invincible % 8 < 4:
            pygame.draw.rect(screen, self.color, player_rect)

            # Глаза
            eye_x = player_rect.x + (30 if self.direction == 1 else 10)
            pygame.draw.circle(screen, (255, 255, 255),
                               (eye_x, player_rect.y + 15), 8)
            pygame.draw.circle(screen, (0, 0, 0),
                               (eye_x, player_rect.y + 15), 4)

        # Рисование жизней
        for i in range(self.lives):
            life_rect = pygame.Rect(20 + i * 40, 20, 30, 30)
            pygame.draw.rect(screen, (255, 50, 50), life_rect)
            pygame.draw.rect(screen, (200, 0, 0), life_rect, 3)

class Platform: # Платформы по которым будет передвигаться персонаж
    def __init__(self, x, y, width, height, type="normal", move_range=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type  # normal, moving, breakable, bouncy
        self.move_range = move_range
        self.move_direction = 1
        self.original_x = x
        self.original_y = y
        self.color = self.get_color()

    def get_color(self): # Типы платформ
        if self.type == "normal":
            return (100, 180, 100)
        elif self.type == "moving":
            return (100, 150, 200)
        elif self.type == "breakable":
            return (180, 120, 80)
        elif self.type == "bouncy":
            return (220, 100, 220)
        return (150, 150, 150)

    def update(self):
        if self.type == "moving" and self.move_range > 0:
            self.x += 2 * self.move_direction
            if abs(self.x - self.original_x) >= self.move_range:
                self.move_direction *= -1

    def draw(self, screen, camera_x, camera_y):
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                           self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 2)

class Enemy: # Враги, которые мешают прохождению уровней
    def __init__(self, x, y, patrol_range=0):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.patrol_range = patrol_range
        self.move_direction = 1
        self.original_x = x
        self.speed = 2
        self.color = (255, 50, 50)

    def update(self): # Движение
        if self.patrol_range > 0:
            self.x += self.speed * self.move_direction
            if abs(self.x - self.original_x) >= self.patrol_range:
                self.move_direction *= -1

    def draw(self, screen, camera_x, camera_y): # Рисование врага
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                           self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        # Глаза врага
        eye_offset = 10 if self.move_direction == 1 else -10
        pygame.draw.circle(screen, (255, 255, 255),
                           (rect.x + 20 + eye_offset, rect.y + 15), 8)
        pygame.draw.circle(screen, (0, 0, 0),
                           (rect.x + 20 + eye_offset, rect.y + 15), 4)

class Goal: # Зона финиша, уровень пройден
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.color = (255, 215, 0)
        self.animation = 0

    def update(self):
        self.animation += 0.1

    def draw(self, screen, camera_x, camera_y):
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                           self.width, self.height)

        # Анимация мерцания
        alpha = int(128 + 127 * abs(pygame.math.Vector2(0, 1).rotate(self.animation * 50).y))
        color = (255, 215, 0) if alpha > 180 else (255, 255, 200)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (200, 160, 0), rect, 4)

        # Надпись FINISH
        font = pygame.font.SysFont(None, 24)
        text = font.render("FINISH", True, (50, 50, 50))
        text_rect = text.get_rect(center=(rect.x + self.width // 2, rect.y + self.height // 2))
        screen.blit(text, text_rect)

class Game: # Запуск, обновление, создание игры (основы)
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.current_level = 0
        self.level_complete = False
        self.paused = False
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        # Загрузка уровней
        self.levels = levels
        self.load_level(self.current_level)

    def load_level(self, level_index):
        level_data = self.levels[level_index]

        # Создание игрока
        self.player = Player(level_data["player_start"][0], level_data["player_start"][1])

        # Создание платформ
        self.platforms = []
        for platform_data in level_data["platforms"]:
            platform = Platform(*platform_data)
            self.platforms.append(platform)

        # Создание врагов
        self.enemies = []
        for enemy_data in level_data.get("enemies", []):
            enemy = Enemy(*enemy_data)
            self.enemies.append(enemy)

        # Создание цели
        self.goal = Goal(*level_data["goal"])

        # Камера
        self.camera_x = 0
        self.camera_y = 0

        # Сброс состояния
        self.level_complete = False
        
    def update(self):
        if self.level_complete or self.paused:
            return

        # Обновление игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(1)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.jump()

        # Обновление объектов
        self.player.update(self.platforms, self.enemies)

        for platform in self.platforms:
            platform.update()

        for enemy in self.enemies:
            enemy.update()

        self.goal.update()

        # Проверка достижения цели
        if self.player.check_collision(self.goal):
            self.level_complete = True

        # Проверка жизней
        if self.player.lives <= 0:
            self.reset_level()

        # Обновление камеры
        self.camera_x = self.player.x - self.width // 2
        self.camera_y = self.player.y - self.height // 2

        # Ограничение камеры
        self.camera_x = max(0, min(self.camera_x, 2000 - self.width))
        self.camera_y = max(0, min(self.camera_y, 2000 - self.height))

        def draw(self):
        # Фон
        self.screen.fill((135, 206, 235))  # Небо

        # Рисование облаков
        for i in range(5):
            x = (i * 400 - self.camera_x // 2) % 2000
            y = 100 + (i * 50) % 150
            pygame.draw.ellipse(self.screen, (255, 255, 255),
                                (x - self.camera_x // 4, y - self.camera_y // 4, 150, 60))

        # Рисование объектов
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x, self.camera_y)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        self.goal.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Интерфейс
        level_text = self.font.render(f"Уровень: {self.current_level + 1}/10", True, (50, 50, 50))
        self.screen.blit(level_text, (self.width - 200, 20))


