import pygame.font


class Button:

    def __init__(self, game, message, text_color=None, button_color=None):
        """Init button attributes"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # configure button dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0) if not button_color else button_color
        self.text_color = (255, 255, 255, 0) if not text_color else text_color
        self.font = pygame.font.Font("assets/fonts/mandalore.otf", 48)

        # generates the rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # assign button message
        self._prep_msg(message)

    def draw_button(self):
        # draws the button
        # self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)

    def _prep_msg(self, message):
        self.message_image = self.font.render(message, True, self.text_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center
