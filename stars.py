import random

import pygame


class Stars:
    def __init__(self, game):
        self.screen = game.screen
        self.star_layers = []
        self.star_speeds = [0.09, 0.1, 0.2]
        self.star_radius = [0.5, 1, 2]

    def set_stars(self):
        for i in range(3):
            star_layer = []
            for _ in range(100):
                x = random.randint(0, self.screen.get_width())
                y = random.randint(0, self.screen.get_height())
                r = self.star_radius[i]

                star_layer.append((x, y, r))

            self.star_layers.append(star_layer)

    def draw_stars(self):
        for i in range(3):
            for star_index in range(len(self.star_layers[i])):
                star = self.star_layers[i][star_index]
                new_y = star[1] + self.star_speeds[i]
                if new_y > self.screen.get_height():
                    new_y = 0
                    star = (random.randint(0, self.screen.get_width()), new_y, star[2])
                else:
                    star = (star[0], new_y, star[2])

                self.star_layers[i][star_index] = star

                pygame.draw.circle(self.screen, (255, 255, 255), (star[0], star[1]), star[2])

