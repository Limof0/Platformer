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
        self.direction = 1  # 1 - вправо, -1 - влево