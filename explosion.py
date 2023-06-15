import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, game, position):
        super().__init__()

        self.game = game
        sprite_sheet = pygame.image.load("assets/sprites/explosion.png")
        frame_width, frame_height = 48, 48
        self.frames = []

        for y in range(0, sprite_sheet.get_height(), frame_height):
            for x in range(0, sprite_sheet.get_width(), frame_width):
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                self.frames.append(frame)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = 10
        self.animation_counter = 0

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
