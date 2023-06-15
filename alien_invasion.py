import sys
import pygame
from time import sleep

from explosion import Explosion
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from sounds import Sounds
from stars import Stars


class AlienInvasion:
    """Main class of the game"""

    def __init__(self, settings):
        """Initialize game and resources"""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        icon = pygame.image.load("assets/sprites/ship_4.png")
        pygame.display.set_icon(icon)
        self.settings = settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.stars = Stars(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.sounds = Sounds()

        # initialize stars
        self.stars.set_stars()

        # init background music
        self.sounds.play_sound(self.sounds.background_sound, 0.1, infinite=True)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        self._create_fleet()

        # creates the play button
        self.play_button = Button(self, "Play Game")
        self.pause_button = Button(self, "Game Paused", text_color=(255, 0, 0), button_color=self.settings.bg_color)

    def run_game(self) -> None:
        """Init the game"""
        while True:
            self._check_events()

            if self.stats.game_active and not self.stats.game_paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self) -> None:
        """Looks for keyboard and mouse inputs to close the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button_click(mouse_position)

    def _check_keydown_events(self, event) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.is_moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.is_moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_j:
            self._start_game()
        elif event.key == pygame.K_p:
            self._pause_game()

    def _check_keyup_events(self, event) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.is_moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.is_moving_left = False

    def _start_game(self):
        if not self.stats.game_active:
            pygame.mouse.set_visible(False)
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.scoreboard.prepare_ships()

            # delete aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # creates a fleet and centers the ship
            self._create_fleet()
            self.ship.center_ship()

    def _pause_game(self):
        # only change pause state if the game is active
        if self.stats.game_active:
            self.stats.game_paused = True if not self.stats.game_paused else False

    def _check_play_button_click(self, mouse_position):
        """Initialize the game when the user clicks the button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self._start_game()

    def _update_screen(self) -> None:
        """Updates the screen"""
        # change background color of the frame
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # draw stars
        self.stars.draw_stars()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self._draw_explosions()

        # draws scoreboard
        self.scoreboard.show_score()

        # draws the button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        else:  # only show pause button if the game is active
            if self.stats.game_paused:
                self.pause_button.draw_button()

        # Draw the frame
        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_cadence and self.stats.game_active and not self.stats.game_paused:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.play_sound(self.sounds.bullet_sound)

    def _remove_bullets(self):
        """remove bullets from the array of bullets"""
        if len(self.bullets) > 0:
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

    def _update_bullets(self):
        """update bullet positions and remove the bullets that aren't showed in screen"""
        self.bullets.update()
        self._remove_bullets()

        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        # check bullets that collides with any alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, dokilla=True, dokillb=True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    # generate explosions
                    explosion = Explosion(self, (alien.rect.centerx, alien.rect.centery))
                    self.explosion_group.add(explosion)
                    self.sounds.play_sound(self.sounds.explosion_sound)

            self.scoreboard.prepare_score()
            self.scoreboard.check_high_score()

        # if there are no more aliens, destroy any bullets and create a new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.scoreboard.prepare_level()
            self.scoreboard.prepare_max_settings_reach()

    def _draw_explosions(self):
        self.explosion_group.update()
        self.explosion_group.draw(self.screen)

    def _create_fleet(self):
        """Creates the fleet of aliens"""
        _alien = Alien(self)
        alien_width, alien_height = _alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        how_many_aliens_per_line = available_space_x // (2 * alien_width)

        # check how many alien lines can be rendered in the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (15 * alien_height) - ship_height
        rows = available_space_y // (2 * alien_height)

        for row in range(rows):
            for col in range(how_many_aliens_per_line):
                self._create_alien(row, col)

    def _create_alien(self, row, col):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * col
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * row)
        self.aliens.add(alien)

    def _update_aliens(self):
        """updates all alien positions"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """checks if an alien touch the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """handles ship hit"""
        # check if the game should still active before remove a live
        if self.stats.ship_lives > 0:
            # remove one live
            self.stats.ship_lives -= 1
            self.scoreboard.prepare_ships()

            # remove all bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            # creates a new fleet and center the ship
            self._create_fleet()

            # center the ship
            self.ship.center_ship()

            # generate the explosion at the ship position
            explosion = Explosion(self, (self.ship.rect.centerx, self.ship.rect.centery))
            self.explosion_group.add(explosion)

            # pauses the game
            sleep(0.5)

            # reproduce sound after the game was un paused
            self.sounds.play_sound(self.sounds.ship_explosion_sound)
        else:
            pygame.mouse.set_visible(True)
            self.stats.game_active = False

            # save high-score if necessary
