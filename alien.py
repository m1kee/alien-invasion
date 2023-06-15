import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Alien stuff"""

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # loads the alien sprite image and configure the rect
        self.image = pygame.image.load('assets/sprites/ship_5.png')
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()

        # initialize an alien in the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # stores the exact position of the alien
        self.x = float(self.rect.x)

    def update(self):
        """moves the alien to the right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """returns true if the alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
