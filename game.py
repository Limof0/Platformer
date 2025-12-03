import pygame
import random


class Player:
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
