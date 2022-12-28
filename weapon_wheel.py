from weapon import *
import pygame


# manages player weapons
class WeaponWheel:
    def __init__(self, game):
        self.game = game
        self.weapons = []
        self.add_weapon(Shotgun(self.game))
        self.add_weapon(Chainsaw(self.game))
        self.current_index = 0
        self.equipped_weapon = self.weapons[0]

    def change_weapon(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                if self.current_index == 1:
                    self.current_index = 0
                else:
                    self.current_index += 1
                self.equipped_weapon = self.weapons[self.current_index]
                self.equipped_weapon.draw()

    def add_weapon(self, weapon):
        self.weapons.append(weapon)
