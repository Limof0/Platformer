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
        self.bounce_multiplier = 1.0  # Множитель отскока

    
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
        self.bounce_multiplier = 1.0  # Сброс множителя отскока

        # Проверка коллизий по Y
        for platform in platforms:
            if self.check_collision(platform):
                if self.vel_y > 0:
                    self.y = platform.y - self.height

                     # Обработка прыгучих платформ
                    if platform.type == "bouncy":
                        # Увеличиваем отскок в 1.5 раза
                        self.vel_y = -self.jump_power * 1.3
                        self.bounce_multiplier = 1.3
                    else:
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
            self.reset_position()
            if self.lives == 1:
                self.lives += 2
            if self.lives == 2:
                self.lives += 1
            if self.lives == 3:
                self.lives += 0


        # Трение
        self.vel_x *= 0.9

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power * self.bounce_multiplier

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
        self.bounce_multiplier = 1.0 

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
        self.bounce_animation = 0  # Для анимации прыгучей платформы

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

        # Анимация для прыгучей платформы
        if self.type == "bouncy":
            self.bounce_animation = (self.bounce_animation + 0.3) % (3.14159 * 2)

    def draw(self, screen, camera_x, camera_y):
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                           self.width, self.height)

        # Специальное отображение для прыгучей платформы
        if self.type == "bouncy":
            # Анимация сжатия/растяжения
            bounce_offset = int(2 * abs(pygame.math.Vector2(0, 1).rotate(self.bounce_animation * 50).y))
            bounce_rect = pygame.Rect(
                self.x - camera_x,
                self.y - camera_y + bounce_offset,
                self.width,
                self.height - bounce_offset * 2
            )

            pygame.draw.rect(screen, self.color, bounce_rect)
            pygame.draw.rect(screen, (180, 80, 200), bounce_rect, 3)


             # Рисуем пружины по бокам
            for i in range(3):
                spring_x1 = bounce_rect.x + 10
                spring_x2 = bounce_rect.x + bounce_rect.width - 10
                spring_y = bounce_rect.y + bounce_rect.height - 10 - i * 10
                pygame.draw.line(screen, (100, 100, 100),
                                (spring_x1, spring_y),
                                (spring_x1, spring_y + 10), 3)
                pygame.draw.line(screen, (100, 100, 100),
                                (spring_x2, spring_y),
                                (spring_x2, spring_y + 10), 3)


        else:
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

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.collected = False
        self.animation = 0
        self.spin_speed = 0.1

    def update(self):
        if not self.collected:
            self.animation += self.spin_speed

    def draw(self, screen, camera_x, camera_y):
        if not self.collected:
            # Позиция с учетом камеры
            screen_x = self.x - camera_x
            screen_y = self.y - camera_y

            # Анимация подпрыгивания
            bounce = abs(pygame.math.Vector2(0, 1).rotate(self.animation * 50).y) * 3

            # Центр монеты
            center_x = screen_x + self.width // 2
            center_y = screen_y + self.height // 2 - bounce

            # Рисуем монету
            pygame.draw.circle(screen, (255, 215, 0),
                               (int(center_x), int(center_y)),
                               self.width // 2)

            # Внутренний круг для эффекта объема
            pygame.draw.circle(screen, (255, 235, 100),
                               (int(center_x), int(center_y)),
                               self.width // 3)

            # Буква "G"
            font = pygame.font.SysFont(None, 20)
            text = font.render("G", True, (100, 80, 0))
            text_rect = text.get_rect(center=(int(center_x), int(center_y)))
            screen.blit(text, text_rect)

            # Свечение монеты
            glow_radius = int(15 + 5 * abs(pygame.math.Vector2(0, 1).rotate(self.animation * 30).y))
            pygame.draw.circle(screen, (255, 255, 200),
                               (int(center_x), int(center_y)),
                               glow_radius, 1)

    def check_collision(self, player):
        if self.collected:
            return False

        return (player.x < self.x + self.width and
                player.x + player.width > self.x and
                self.y < player.y + player.height and
                self.y + self.height > player.y)

class Game: # Запуск, обновление, создание игры (основы)
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.current_level = 0
        self.level_complete = False
        self.paused = False
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        # Статистика
        self.total_coins = 10  # Всего монет в игре
        self.coins_collected = 0  # Собранные монеты
        self.level_coins_collected = 0  # Монеты на текущем уровне
        self.coin_sound_played = False  # Флаг для звука

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
        self.level_coins_collected = 0
        self.coin_sound_played = False
        
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
        self.coin.update()

        # Проверка сбора монеты
        if not self.coin.collected and self.coin.check_collision(self.player):
            self.coin.collected = True
            self.coins_collected += 1
            self.level_coins_collected = 1

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
        self.camera_y = max(-100, min(self.camera_y, 3000 - self.height))

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
        self.coin.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Интерфейс
        level_text = self.font.render(f"Уровень: {self.current_level + 1}/10", True, (50, 50, 50))
        self.screen.blit(level_text, (self.width - 200, 20))

        # Отображение монет
        coin_text = self.font.render(f"Монеты: {self.coins_collected}/{self.total_coins}", True, (50, 50, 50))
        self.screen.blit(coin_text, (self.width - 200, 60))

        # Индикатор монеты на текущем уровне
        if not self.coin.collected:
            coin_status = self.small_font.render("Монета не собрана", True, (180, 50, 50))
        else:
            coin_status = self.small_font.render("Монета собрана!", True, (50, 180, 50))
        self.screen.blit(coin_status, (self.width - 200, 100))

        # Анимация сбора монеты
        if self.coin.collected and not self.coin_sound_played:
            # Визуальный эффект при сборе монеты
            effect_radius = 50
            pygame.draw.circle(self.screen, (255, 255, 200, 150),
                               (self.width // 2, self.height // 2),
                               effect_radius, 3)
            self.coin_sound_played = True

        # Сообщение о завершении уровня
        if self.level_complete:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            complete_text = self.font.render("Уровень пройден!", True, (255, 255, 255))

            # Информация о монетах
            coins_info = f"Монеты: {self.coins_collected}/{self.total_coins}"
            coins_text = self.small_font.render(coins_info, True, (255, 255, 150))

            if self.current_level < 9:
                next_text = self.small_font.render("Нажмите N для следующего уровня", True, (200, 200, 255))
            else:
                next_text = self.small_font.render("Игра пройдена! Поздравляем!", True, (200, 255, 200))


            self.screen.blit(complete_text,
                             (self.width // 2 - complete_text.get_width() // 2,
                              self.height // 2 - 80))
            self.screen.blit(coins_text,
                             (self.width // 2 - coins_text.get_width() // 2,
                              self.height // 2 - 30))
            self.screen.blit(next_text,
                             (self.width // 2 - next_text.get_width() // 2,
                              self.height // 2 + 20))

        # Пауза
        if self.paused:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            pause_text = self.font.render("ПАУЗА", True, (255, 255, 255))
            self.screen.blit(pause_text,
                             (self.width // 2 - pause_text.get_width() // 2,
                              self.height // 2 - 30))

            info_text = self.small_font.render("Управление: ← → или A D - движение, SPACE - прыжок", True,
                                               (200, 200, 200))
            info_text2 = self.small_font.render("R - перезапуск уровня, P - пауза, ESC - выход", True, (200, 200, 200))
            self.screen.blit(info_text,
                             (self.width // 2 - info_text.get_width() // 2,
                              self.height // 2 + 30))
            self.screen.blit(info_text2,
                             (self.width // 2 - info_text2.get_width() // 2,
                              self.height // 2 + 60))

    def next_level(self): #Следующий уровень
        if self.current_level < 9 and self.level_complete:
            self.current_level += 1
            self.load_level(self.current_level)

    def reset_level(self): #Рестарт уровня
        self.load_level(self.current_level)

























