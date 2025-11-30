import math
import random

import pygame
from pygame.sprite import Sprite


class Alien_4(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        self.image = pygame.image.load('images/alien_a3.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = ai_game.settings.alien_speed
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(-125, -115)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        dx = self.ship.rect.x - self.rect.centerx
        dy = self.ship.rect.y - self.rect.centery
        distance = math.hypot(dx, dy)
        self.x += dx / distance * self.speed * 3
        self.y += dy / distance * self.speed * 3
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

