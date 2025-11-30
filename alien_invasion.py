import json
import sys
from pathlib import Path
from time import sleep

import pygame

from alien_1 import Alien_1
from alien_2 import Alien_2
from alien_3 import Alien_3
from alien_4 import Alien_4
from alien_boss import Alien_boss
from alien_fleet import Alien_Fleet
from bullet import Bullet
from button import Button
from eggs import Eggs
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from text import CenterTopText


class AlienInvasion:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/bgmusic.ogg')
        pygame.mixer.music.play(-1)
        self.sound_effect1 = pygame.mixer.Sound('sounds/fisound.wav')
        self.sound_effect2 = pygame.mixer.Sound('sounds/exsound.wav')
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.st_background_image = self.settings.st_background_image
        pygame.transform.scale(self.st_background_image, (self.settings.screen_width, self.settings.screen_height))
        self.level_1_bg_image = self.settings.level_1_bg_image
        pygame.transform.scale(self.level_1_bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.level_2_bg_image = self.settings.level_2_bg_image
        pygame.transform.scale(self.level_2_bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.level_3_bg_image = self.settings.level_3_bg_image
        pygame.transform.scale(self.level_3_bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.level_4_bg_image = self.settings.level_4_bg_image
        pygame.transform.scale(self.level_4_bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.fi_background_image = self.settings.fi_background_image
        pygame.transform.scale(self.fi_background_image, (self.settings.screen_width, self.settings.screen_height))
        self.egg_background_image = self.settings.egg_background_image
        pygame.transform.scale(self.egg_background_image, (self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.title = CenterTopText(self.screen, "Alien Invasion", 180, (255, 255, 255), 60)
        self.over = CenterTopText(self.screen, "Congratulations! But not over.", 80, (255, 255, 255),
                                  self.settings.screen_height * 0.5 + 20)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.alien_boss = Alien_boss(self)
        self._create_ship()
        self.bullets = pygame.sprite.Group()
        self.aliens_fleet = pygame.sprite.Group()
        self.alien_1 = pygame.sprite.GroupSingle()
        self.alien_2 = pygame.sprite.GroupSingle()
        self.alien_3 = pygame.sprite.GroupSingle()
        self.alien_4 = pygame.sprite.GroupSingle()
        self.alien_boss = pygame.sprite.GroupSingle()
        self._create_fleet()
        self._create_alien_1()
        self._create_alien_2()
        self._create_alien_3()
        self._create_alien_4()
        self._create_alien_boss()
        self.game_active = False
        self.game_paused = False
        self.game_over = False
        self.play_button = Button(self, "START")
        self.eggs = Eggs(self, "Congratulations! Escape the chains and triumph.")

    def run_game(self):

        while True:
            self._check_events()
            if self.game_active and not self.game_paused:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._check_level()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) < self.settings.bullets_allowed:
                self.sound_effect1.play()
                self.sound_effect1.set_volume(0.2)
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_p:
            self._toggle_pause()

    def _check_level(self):
        if self.stats.level in {1, 3, 5, 7}:
            self._update_alien_1()
            self._update_alien_2()
            self._update_alien_3()
        elif self.stats.level in {2, 4, 6, 8}:
            self._update_aliens_fleet()
        elif self.stats.level == 9:
            self._update_alien_boss()
            self._update_alien_4()

    def _toggle_pause(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.show_level = True
            self.stats.level_start_time = pygame.time.get_ticks()
            self.stats.pending_create_aliens = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.alien_1.empty()
            self.alien_2.empty()
            self.alien_3.empty()
            self.aliens_fleet.empty()
            self.alien_boss.empty()
            self._create_aliens_based_on_level()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_aliens_based_on_level(self):
        if self.stats.level in {1, 3, 5, 7}:
            self.alien_1.empty()
            self.alien_2.empty()
            self.alien_3.empty()
            self._create_alien_1()
            self._create_alien_2()
            self._create_alien_3()
        elif self.stats.level in {2, 4, 6, 8}:
            self.aliens_fleet.empty()
            self._create_fleet()
        elif self.stats.level == 9:
            self.alien_boss.empty()
            self._create_alien_boss()
            self._create_alien_4()

    def _create_ship(self):
        if self.ship:
            self.ship.kill()
        self.ship = Ship(self)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        if self.stats.level in {1, 3, 5, 7}:
            self._check_bullet_alien_1_2_3_collision()
        elif self.stats.level in {2, 4, 6, 8}:
            self._check_bullet_alien_collision()
        else:
            self._check_bullet_alien_4_collision()
            self._check_bullet_alien_boss_collision()

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens_fleet, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens_fleet and self.stats.level in {2, 4, 6, 8}:
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self.ship.blimte()
            self.sb.prep_level()
            self.stats.show_level = True
            self.stats.level_start_time = pygame.time.get_ticks()
            self._create_ship()
            self.sb.prep_ships()
            self._create_alien_1()
            self._create_alien_2()
            self._create_alien_3()
            self._create_alien_boss()

    def _check_bullet_alien_1_2_3_collision(self):
        collisions_1 = pygame.sprite.groupcollide(self.bullets, self.alien_1, True, True)
        collisions_2 = pygame.sprite.groupcollide(self.bullets, self.alien_2, True, True)
        collisions_3 = pygame.sprite.groupcollide(self.bullets, self.alien_3, True, True)
        if collisions_1 or collisions_2 or collisions_3:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
            if not hasattr(self, 'count'):
                self.count = 1
            if self.count < 3:
                if not self.alien_1 and not self.alien_2 and not self.alien_4 and self.stats.level in {1, 3, 5, 7}:
                    self._create_alien_1()
                    self._create_alien_2()
                    self._create_alien_3()
                    self.count += 1
        while not self.alien_1 and not self.alien_2 and self.stats.level in {1, 3, 5, 7}:
            self.bullets.empty()
            self.settings.increase_speed()
            self.count = 1
            self.ship.blimte()
            self.stats.level += 1
            self.sb.prep_level()
            self.stats.show_level = True
            self.stats.level_start_time = pygame.time.get_ticks()
            self._create_ship()
            self.sb.prep_ships()
            self._create_fleet()

    def _check_bullet_alien_4_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien_4, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not hasattr(self, 'count'):
            self.count = 1
        if self.count < 50:
            if not self.alien_4 and self.stats.level == 9:
                self._create_alien_4()
                self.count += 1

    def _check_bullet_alien_boss_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien_boss, True, False)
        if collisions:
            alien_boss = Alien_boss(self)
            self.settings.alien_boss_health -= 25
            alien_boss.draw_health_bar()
            if self.settings.alien_boss_health < 500:
                alien_boss.update_phase()
            if alien_boss.boss_dead():
                self.game_over = True

    def _create_alien(self, x_position, y_position):
        new_alien = Alien_Fleet(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens_fleet.add(new_alien)

    def _create_fleet(self):
        alien = Alien_Fleet(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _update_aliens_fleet(self):
        self._check_fleet_edges()
        self.aliens_fleet.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens_fleet):
            self._ship_hit()
        self._check_alien_fleet_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens_fleet.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens_fleet.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien_1(self):
        alien_1 = Alien_1(self)
        self.alien_1.add(alien_1)

    def _update_alien_1(self):
        self.alien_1.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_1):
            self._ship_hit()
        for alien in self.alien_1.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_alien_2(self):
        alien_2 = Alien_2(self)
        self.alien_2.add(alien_2)

    def _update_alien_2(self):
        self.alien_2.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_2):
            self._ship_hit()
        for alien in self.alien_2.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_alien_3(self):
        alien_3 = Alien_3(self)
        self.alien_3.add(alien_3)

    def _update_alien_3(self):
        self.alien_3.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_3):
            self._ship_hit()
        for alien in self.alien_3.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_alien_4(self):
        alien_4 = Alien_4(self)
        self.alien_4.add(alien_4)

    def _update_alien_4(self):
        self.alien_4.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_4):
            self._ship_hit()
        for alien in self.alien_4.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()

    def _create_alien_boss(self):
        alien_boss = Alien_boss(self)
        self.alien_boss.add(alien_boss)

    def _update_alien_boss(self):
        self.alien_boss.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_boss):
            self._ship_hit()
        for alien in self.alien_boss.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.settings.alien_boss_y_direction *= -1
            if alien.rect.top <= 0:
                self.settings.alien_boss_y_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.sound_effect2.play()
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self._create_aliens_based_on_level()
            self.ship.center_ship()

            sleep(0.35)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_alien_fleet_bottom(self):
        for alien in self.aliens_fleet.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _draw_pause_message(self):
        font = pygame.font.SysFont('Impact', 52)
        msg_image = font.render("Game Paused. Press P to resume.", True,
                                (0, 0, 0))
        msg_rect = msg_image.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(msg_image, msg_rect)

    def _update_screen(self):
        if not self.game_active:
            self.screen.blit(self.st_background_image, (0, 0))
        elif self.stats.level in {1, 2}:
            self.screen.blit(self.level_1_bg_image, (0, 0))
        elif self.stats.level in {3, 4}:
            self.screen.blit(self.level_2_bg_image, (0, 0))
        elif self.stats.level in {5, 6}:
            self.screen.blit(self.level_3_bg_image, (0, 0))
        elif self.stats.level in {7, 8}:
            self.screen.blit(self.level_4_bg_image, (0, 0))
        elif self.stats.level == 9:
            self.screen.blit(self.fi_background_image, (0, 0))

        if self.game_active:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blimte()
            if self.stats.level in {1, 3, 5, 7}:
                self.alien_1.draw(self.screen)
                self.alien_2.draw(self.screen)
                self.alien_3.draw(self.screen)
            elif self.stats.level in {2, 4, 6, 8}:
                self.aliens_fleet.draw(self.screen)
            elif self.stats.level == 9:
                alien_boss = Alien_boss(self)
                alien_boss.draw_health_bar()
                self.alien_boss.draw(self.screen)
                self.alien_4.draw(self.screen)
                if pygame.sprite.groupcollide(self.bullets, self.alien_boss, True, False):
                    alien_boss.draw_health_bar()
            self.sb.show_score()
        if not self.game_active:
            self.title.draw()
            self.play_button.draw_button()
        if self.ship.free_ship() and self.stats.level == 9:
            self.game_active = False
            self.screen.blit(self.egg_background_image, (0, 0))
            pygame.mouse.set_visible(True)
            self.eggs.draw_eggs()
        if self.game_over:
            self.screen.blit(self.st_background_image, (0, 0))
            self.over.draw()
        if self.game_paused:
            self._draw_pause_message()

        if self.stats.show_level:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.stats.level_start_time
            display_duration = 1600
            if elapsed_time < display_duration:
                level_str = f"LEVEL {self.stats.level}"
                self.font = pygame.font.SysFont('Impact', 136)
                level_image = self.font.render(level_str, True, (255, 255, 255))
                alpha = 255 - int((elapsed_time / 1500) * 255) + 20
                level_image = level_image.convert_alpha()
                level_image.set_alpha(alpha)
                level_rect = level_image.get_rect()
                level_rect.center = self.screen.get_rect().center
                self.screen.blit(level_image, level_rect)
            else:
                self.stats.show_level = False

        pygame.display.flip()

    def _close_game(self):
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)

        sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
