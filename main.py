import pygame
import sys
from settings import *
from map import *
from player import *
from ray_casting import *


class Game:
    def __init__(self):
        self.ray_cast = None
        self.player = None
        self.map = None
        pygame.init()
        self.screen = pygame.display.set_mode(Res)
        self.clock = pygame.time.Clock()
        self.delta = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.ray_cast = RayCasting(self)

    def update_screen(self):
        self.player.update()
        self.ray_cast.update()
        pygame.display.flip()
        self.delta = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill('black')
        #self.map.test_draw()
        #self.player.test_draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update_screen()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
