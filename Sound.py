import pygame


class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = 'resources/sounds/'
        self.shotgun = pygame.mixer.Sound(self.path + 'sound_shotgun.wav')
