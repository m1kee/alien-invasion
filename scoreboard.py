import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """Shows player information"""

    def __init__(self, game):
        """Initialize game score"""
        self.max_settings_reach_rect = None
        self.max_settings_reach_image = None
        self.ships = None
        self.level_rect = None
        self.level_image = None
        self.high_score_rect = None
        self.high_score_image = None
        self.score_rect = None
        self.score_image = None

        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # font configuration
        self.text_color = (255, 255, 255, 0)
        self.font = pygame.font.Font("assets/fonts/mandalore.otf", 48)
        #  self.font = pygame.font.SysFont('', 48)

        # prepare image of the score
        self.prepare_score()
        self.prepare_high_score()
        self.prepare_level()
        self.prepare_ships()
        self.prepare_max_settings_reach()

    def prepare_score(self):
        """Converts the score into an image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(f"SCORE: {score_str}", True, self.text_color)

        # shows the score in the top right corner of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 28  # to have a margin of 28px
        self.score_rect.top = 20  # 20px margin top

    def prepare_high_score(self):
        """Converts the high score into an image"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(
            f"HIGH SCORE: {high_score_str}",
            True,
            self.text_color
        )

        # shows the score in the top right corner of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20  # 20px margin top

    def prepare_level(self):
        """Converts the level into an image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            f"LEVEL: {level_str}",
            True,
            self.text_color
        )

        # shows the score in the top right corner of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  # to have 10px margin bottom from the score

    def prepare_max_settings_reach(self):
        # max_ship_velocity_reached = "YES" if self.settings.ship_speed >= self.settings.max_ship_speed else "NO"
        # max_bullet_velocity_reached = "YES" if self.settings.bullet_speed >= self.settings.max_bullet_speed else "NO"
        # max_alien_velocity_reached = "YES" if self.settings.alien_speed >= self.settings.max_alien_points else "NO"
        # max_points_per_alien_reached = "YES" if self.settings.alien_points >= self.settings.max_alien_points else "NO"
        #
        # self.max_settings_reach_image = self.font.render(
        #     f"MAX SHIP VEL: {max_ship_velocity_reached} - MAX BULLET VEL: {max_bullet_velocity_reached} - MAX ALIEN "
        #     f"VEL: {max_alien_velocity_reached} - MAX POINTS PER ALIEN: {max_points_per_alien_reached}",
        #     True,
        #     self.text_color
        # )

        self.max_settings_reach_image = self.font.render(
            f"SHIP VEL: {self.settings.ship_speed:.2f} - BULLET VEL: {self.settings.bullet_speed:.2f} - ALIEN "
            f"VEL: {self.settings.alien_speed:.2f} - POINTS PER ALIEN: {self.settings.alien_points:.2f}",
            True,
            self.text_color
        )
        
        self.max_settings_reach_rect = self.max_settings_reach_image.get_rect()
        self.max_settings_reach_rect.left = self.screen_rect.left + 10
        self.max_settings_reach_rect.bottom = self.screen_rect.bottom - 10

    def prepare_ships(self):
        """Converts the ship lives into an image"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_lives):
            ship = Ship(self.game)
            ship.rect.x = 10 + (ship_number * ship.rect.width)
            ship.rect.y = 20
            self.ships.add(ship)

    def show_score(self):
        """Draws the score in the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.max_settings_reach_image, self.max_settings_reach_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """check if the current score if higher than high_score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prepare_high_score()
