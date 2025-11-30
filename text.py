import pygame
import pygame.font


class CenterTopText:
    def __init__(self, screen, text, font_size, color, y_offset):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.font_size = font_size
        self.color = color
        self.y_offset = y_offset
        self.font = pygame.font.SysFont('Impact', self.font_size)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centerx = self.screen_rect.centerx
        self.text_rect.top = self.y_offset

    def draw(self):
        self.screen.blit(self.text_surface, self.text_rect)