import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """All the ship stuff"""

    def __init__(self, game):
        """Init the ship and configure the initial position"""
        super().__init__()
        
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Loads the ship sprite and get its rect
        self.image = pygame.image.load('assets/sprites/ship_4.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        y = self.screen_rect.bottom - (48 * 3)

        self.rect.y = y
        self.is_moving_right = False
        self.is_moving_left = False
        self.ship_speed = game.settings.ship_speed
        self.x = float(self.rect.x)
        self.y = y

    def blitme(self):
        """Draws the sprite into its actual position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Moves the ship in the screen based on the x_axis"""
        if self.is_moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed
        if self.is_moving_left and self.rect.left > 0:
            self.x -= self.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """centers the ship in the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)