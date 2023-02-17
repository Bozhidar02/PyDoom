import unittest
from main import *
import pygame
from unittest.mock import Mock


class Test(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()
        self.ray_casting = RayCasting(self.game)
        self.weapon = Weapon(game=self.game, damage=50)
        self.player = Player(self.game)
        self.ammo = Ammo(self.game, pos=(2.5, 3.5), scale=1, shift=0)

    def test_wall_coords_there_is_wall(self, x=0, y=0):
        self.assertEqual(self.game.player.wall_coords(x, y), False)

    def test_wall_coords_there_is_no_wall(self, x=1, y=1):
        self.assertEqual(self.game.player.wall_coords(x, y), True)

    def test_collision_x(self, x=1, y=1):
        self.game.player.collision_check(x, y)
        self.assertEqual(self.game.player.x, 2.5)

    def test_ray_cast(self):
        self.game.player.angle = 0
        self.ray_casting.ray_cast()
        self.assertEqual(len(self.ray_casting.ray_casting_result), NUM_RAYS)
        self.assertEqual(len(self.ray_casting.ray_casting_result[0]), 4)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][0], float)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][1], float)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][2], int)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][3], float)

    def test_weapon_has_correct_attributes(self):
        self.assertEqual(self.weapon.damage, 50)
        self.assertEqual(self.weapon.reloading, False)
        self.assertEqual(self.weapon.num_images, len(self.weapon.images))
        self.assertEqual(self.weapon.frame_counter, 0)
        self.assertEqual(self.weapon.range, 10)

    def test_animate_shot_while_reloading(self):
        self.weapon.reloading = True
        self.weapon.animation_trigger = True
        self.weapon.num_images = 2
        self.weapon.animate_shot()
        # self.assertEqual(self.weapon.images[0], self.weapon.images[-1])
        self.assertEqual(self.weapon.frame_counter, 1)
        self.assertNotEqual(self.weapon.reloading, False)
        self.assertEqual(self.weapon.frame_counter, 1)

    def test_fire_with_left_mouse_click(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        self.player.fire(event)
        self.assertTrue(self.player.shot)

    def test_fire_with_space_bar_press(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.player.fire(event)
        self.assertTrue(self.player.shot)

    def test_take_damage(self):
        initial_health = self.player.health
        self.player.take_damage(10)
        self.assertEqual(self.player.health, initial_health - 5)

    def test_pick_up_adds_ammo_to_weapon(self):
        self.game.player.x = 2.5
        self.game.player.y = 3.5
        self.game.weapons.weapons[0].ammo = 0
        self.game.object_manager.sprites.append(self.ammo)
        self.ammo.pick_up()
        self.assertEqual(self.game.weapons.weapons[0].ammo, 5)

    def test_pick_up_removes_ammo_from_map(self):
        self.ammo.pick_up()
        self.assertNotIn(self.ammo, self.game.object_manager.sprites)

