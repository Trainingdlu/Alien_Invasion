import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        level = int(self.stats.level)
        if level in {1, 2, 3, 4}:
            count = 1
        elif level in {5, 6, 7, 8}:
            count = 2
        elif level == 9:
            count = 3
        else:
            count = 1
        self.image = pygame.image.load(f'images/ship_{count}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top and self.stats.level in {1, 2, 3, 4, 5, 6, 7, 8}:
            self.y -= self.settings.ship_speed
        elif self.stats.level == 9:
            if self.moving_up:
                self.y -= self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blimte(self):
        self.screen.blit(self.image, self.rect)

    def free_ship(self):
        if self.rect.bottom < self.screen_rect.top:
            return True
        return False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

