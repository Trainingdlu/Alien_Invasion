
import random

import pygame
from pygame.sprite import Sprite


class Alien_3(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien_.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = ai_game.settings.alien_speed
        self.speed_y = self.speed * 2.85
        self.direction_3 = 1
        self.rect.x = random.randint(self.settings.screen_width - 800, self.settings.screen_width - 200)
        self.rect.y = random.randint(-70, -60)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        screen_rect = self.screen.get_rect()
        self.y += self.speed_y * 1.25
        self.rect.y = int(self.y)
        if self.x >= screen_rect.right - 60:
            self.x = screen_rect.right - 60
            self.direction_3 *= -1
        elif self.x <= 0:
            self.x = 0
            self.direction_3 *= -1
