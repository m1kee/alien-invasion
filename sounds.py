import pygame.mixer


class Sounds:
    def __init__(self):
        """Init all game sounds"""
        self.background_sound = pygame.mixer.Sound("assets/sounds/background_music.mp3")
        self.bullet_sound = pygame.mixer.Sound("assets/sounds/laser.mp3")
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        self.ship_explosion_sound = pygame.mixer.Sound("assets/sounds/ship_explosion.wav")

    def play_sound(self, sound, volume=0.1, infinite=None):
        if sound:
            sound.set_volume(volume)
            if infinite:
                sound.play(-1)
            else:
                sound.play()
