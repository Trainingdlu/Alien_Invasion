import pygame


class Settings:

    def __init__(self):
        self.st_background_image = pygame.image.load("images/st_background.png")
        self.level_1_bg_image = pygame.image.load("images/level_1_bg.png")
        self.level_2_bg_image = pygame.image.load("images/level_2_bg.png")
        self.level_3_bg_image = pygame.image.load("images/level_3_bg.png")
        self.level_4_bg_image = pygame.image.load("images/level_4_bg.png")
        self.fi_background_image = pygame.image.load("images/fi_background.png")
        self.egg_background_image = pygame.image.load("images/egg_background.png")
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.bullet_speed = 3
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_boss_y_direction = 1
        self.alien_boss_health = 1000
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
