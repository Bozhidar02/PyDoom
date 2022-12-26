import pygame
import sys
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Res)
        self.clock = pygame.time.Clock()


