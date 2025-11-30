
import math
import random

import pygame
from pygame.sprite import Sprite


class Alien_boss(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.images = {
            'phase1': pygame.image.load('images/alien_boss_1.png').convert_alpha(),
            'phase2': pygame.image.load('images/alien_boss_2.png').convert_alpha()
        }
        self.current_image = self.images['phase1']
        self.image = self.current_image
        self.rect = self.image.get_rect(center=(self.screen_rect.centerx, 180))
        self.speed = ai_game.settings.alien_speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed_x = self.speed * 1.5 * random.choice([-1, 1])
        self.speed_y = self.speed * 1.5 * random.choice([-1, 1])
        self.direction_boss = 1
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.max_health = 1000
        self.boss_dead()
        self.last_attacked_time = 0
        self.attack_cooldown = 1500

    def draw_health_bar(self):
        bar_width = 1000
        bar_height = 15
        outline_x = self.screen.get_width() // 2 - bar_width // 2
        outline_rect = pygame.Rect(outline_x, 20, bar_width, bar_height)
        pygame.draw.rect(self.screen, (0, 0, 0), outline_rect)

        health_ratio = self.settings.alien_boss_health / self.max_health
        current_width = bar_width * health_ratio
        fill_rect = pygame.Rect(outline_x, 20, current_width, bar_height)
        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)

    def update_phase(self):
        if self.settings.alien_boss_health < 500:
            if self.current_image != self.images['phase2']:
                old_center = self.rect.center
                self.current_image = self.images['phase2']
                self.image = self.current_image
                self.rect = self.image.get_rect(center=old_center)
        else:
            if self.current_image != self.images['phase1']:
                old_center = self.rect.center
                self.current_image = self.images['phase1']
                self.image = self.current_image
                self.rect = self.image.get_rect(center=old_center)

    def boss_dead(self):
        if self.settings.alien_boss_health <= 0:
            return True

    def update(self):
        screen_rect = self.screen.get_rect()
        self.update_phase()
        self.x += self.direction_boss * self.speed_x
        self.y += self.speed_y * 1.25 * self.settings.alien_boss_y_direction
        sine_offset = math.sin(self.angle)
        self.rect.x = int(self.x + sine_offset)
        self.rect.y = int(self.y)
        self.angle += 0.1
        if self.x >= screen_rect.right - 225:
            self.x = screen_rect.right - 225
            self.direction_boss *= -1
        elif self.x <= 0:
            self.x = 0
            self.direction_boss *= -1
