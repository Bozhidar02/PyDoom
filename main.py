import pygame
import sys
from settings import *
from map import *
from player import *
from ray_casting import *
from object_renderer import *
from object_manager import *
from weapon import *
from Sound import *
from pathfinding import *
from weapon_wheel import *


class Game:
    def __init__(self):
        self.weapons = None
        self.pathfinder = None
        self.sound = None
        self.weapon = None
        self.object_manager = None
        self.animated_sprite = None
        self.static_sprite = None
        self.obj_render = None
        self.ray_cast = None
        self.player = None
        self.map = None
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(Res)
        self.clock = pygame.time.Clock()
        self.delta = 1
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.obj_render = ObjectRenderer(self)
        self.ray_cast = RayCasting(self)
        self.object_manager = ObjectManager(self)
        # self.weapon = Weapon(self)
        self.weapons = WeaponWheel(self)
        self.sound = Sound(self)
        self.pathfinder = Pathfinder(self)

        self.sound.theme.play()
        
    def update_screen(self):
        self.player.update()
        self.ray_cast.update()
        self.object_manager.update()
        self.weapons.equipped_weapon.update()
        pygame.display.flip()
        self.delta = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.obj_render.draw()
        self.weapons.equipped_weapon.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            self.player.fire(event)
            self.weapons.change_weapon(event)


    def run(self):
        while True:
            self.check_events()
            self.update_screen()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
