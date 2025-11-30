import pygame.font


class Button:
    def __init__(self, ai_game, msg, y_offset=-230):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.colors = {'normal': (2, 210, 98), 'hover': (6, 192, 95), 'pressed': (0, 140, 0)}
        self.current_color = self.colors['normal']
        self.state = 'normal'
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('Impact', 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom + y_offset
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos):
            if mouse_clicked:
                self.state = 'pressed'
            else:
                self.state = 'hover'
        else:
            self.state = 'normal'

        self.current_color = self.colors[self.state]
        self.screen.fill(self.current_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
