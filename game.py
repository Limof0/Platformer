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
