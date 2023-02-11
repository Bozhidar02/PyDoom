import unittest
from main import *
import pygame
from unittest.mock import Mock
import weapon


class Test(unittest.TestCase):

    def test_take_damage(self, game=Game()):
        game.player.take_damage(10)
        self.assertEqual(game.player.health, 90)

    def test_wall_coords_there_is_wall(self, x=0, y=0):
        game = Game()
        self.assertEqual(game.player.wall_coords(x, y), False)

    def test_wall_coords_there_is_no_wall(self, x=1, y=1):
        game = Game()
        self.assertEqual(game.player.wall_coords(x, y), True)

    def test_collision_x(self, x=1, y=1):
        game = Game()
        game.player.collision_check(x, y)
        self.assertEqual(game.player.x, 2.5)

    def test_collision_y(self, x=1, y=1):
        game = Game()
        game.player.collision_check(x, y)
        self.assertEqual(game.player.y, 6)


class TestGetPath(unittest.TestCase):

    def setUp(self):
        game = Game()
        self.path_finder = Pathfinder(game)
        self.graph = {(1, 1): [(2, 1), (1, 2), (2, 2)],
                      (2, 1): [(1, 1), (3, 1), (2, 2), (3, 2), (1, 2)],
                      (3, 1): [(2, 1), (4, 1), (3, 2), (4, 2), (2, 2)],
                      (4, 1): [(3, 1), (5, 1), (4, 2), (5, 2), (3, 2)],
                      (5, 1): [(4, 1), (6, 1), (5, 2), (6, 2), (4, 2)],
                      (6, 1): [(5, 1), (7, 1), (6, 2), (7, 2), (5, 2)],
                      (7, 1): [(6, 1), (8, 1), (7, 2), (8, 2), (6, 2)],
                      (8, 1): [(7, 1), (9, 1), (8, 2), (9, 2), (7, 2)],
                      (9, 1): [(8, 1), (10, 1), (9, 2), (10, 2), (8, 2)],
                      (10, 1): [(9, 1), (11, 1), (10, 2), (11, 2), (9, 2)],
                      (11, 1): [(10, 1), (12, 1), (11, 2), (12, 2), (10, 2)],
                      (12, 1): [(11, 1), (13, 1), (12, 2), (13, 2), (11, 2)],
                      (13, 1): [(12, 1), (14, 1), (13, 2), (14, 2), (12, 2)],
                      (14, 1): [(13, 1), (14, 2), (13, 2)], (1, 2): [(1, 1), (2, 2), (1, 3), (2, 1), (2, 3)],
                      (2, 2): [(1, 2), (2, 1), (3, 2), (2, 3), (1, 1), (3, 1), (3, 3), (1, 3)],
                      (3, 2): [(2, 2), (3, 1), (4, 2), (3, 3), (2, 1), (4, 1), (4, 3), (2, 3)],
                      (4, 2): [(3, 2), (4, 1), (5, 2), (4, 3), (3, 1), (5, 1), (5, 3), (3, 3)],
                      (5, 2): [(4, 2), (5, 1), (6, 2), (5, 3), (4, 1), (6, 1), (6, 3), (4, 3)],
                      (6, 2): [(5, 2), (6, 1), (7, 2), (6, 3), (5, 1), (7, 1), (7, 3), (5, 3)],
                      (7, 2): [(6, 2), (7, 1), (8, 2), (7, 3), (6, 1), (8, 1), (8, 3), (6, 3)],
                      (8, 2): [(7, 2), (8, 1), (9, 2), (8, 3), (7, 1), (9, 1), (9, 3), (7, 3)]}

    def test_get_path(self):
        start = (4, 1)
        dest = (1, 1)
        expected_path = (3, 1)
        self.assertEqual(self.path_finder.get_path(start, dest), expected_path)


class TestWeapon(unittest.TestCase):

    def setUp(self):
        self.game = Mock()
        self.weapon = Weapon(game=self.game, damage=50)

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
        #self.assertEqual(self.weapon.images[0], self.weapon.images[-1])
        self.assertEqual(self.weapon.frame_counter, 1)
        self.assertNotEqual(self.weapon.reloading, False)
        self.assertEqual(self.weapon.frame_counter, 1)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()
        self.player = Player(self.game)
        self.weapons = Weapon(self.game)

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
        self.assertEqual(self.player.health, initial_health - 10)
