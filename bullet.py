import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """All bullet stuff"""

    def __init__(self, game):
        """Creates a bullet in the actual ship position"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # create the rect for the bullet and then assign the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        # saves the bullet position as float
        self.y = float(self.rect.y)

    def update(self) -> None:
        """moves the bullet up"""
        # updates the y-axis of the bullet position
        self.y -= self.settings.bullet_speed
        # updates the position of the bullet
        self.rect.y = self.y

    def draw_bullet(self):
        """draws the bullet in the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
