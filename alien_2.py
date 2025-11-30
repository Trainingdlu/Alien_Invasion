
import math
import random

import pygame
from pygame.sprite import Sprite


class Alien_2(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien_a2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = ai_game.settings.alien_speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed_x = self.speed * 2 * random.choice([-1, 1])
        self.speed_y = self.speed * 1.5
        self.direction_2 = 1
        self.rect.x = random.randint(self.settings.screen_width - 600, self.settings.screen_width - 150)
        self.rect.y = random.randint(-145, -120)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        screen_rect = self.screen.get_rect()
        self.x += self.direction_2 * self.speed_x
        self.y += self.speed_y * 1.25
        sine_offset = math.sin(self.angle)
        self.rect.x = int(self.x + sine_offset)
        self.rect.y = int(self.y)
        self.angle += 0.07
        if self.x >= screen_rect.right - 60:
            self.x = screen_rect.right - 60
            self.direction_2 *= -1
        elif self.x <= 0:
            self.x = 0
            self.direction_2 *= -1
