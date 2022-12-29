import pygame


class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = 'resources/sounds/'
        self.shotgun = pygame.mixer.Sound(self.path + 'sound_shotgun.wav')
        self.chainsaw = pygame.mixer.Sound(self.path + 'sound_chainsaw.mp3')
        self.npc_pain = pygame.mixer.Sound(self.path + 'sound_npc_pain.wav')
        self.player_pain = pygame.mixer.Sound(self.path + 'sound_player_pain.wav')
        self.npc_death = pygame.mixer.Sound(self.path + 'sound_npc_death.wav')
        self.npc_attack = pygame.mixer.Sound(self.path + 'sound_npc_death.wav')
        self.theme = pygame.mixer.Sound(self.path + 'theme.mp3')
