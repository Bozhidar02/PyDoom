import unittest
from main import *
import pygame
from unittest.mock import Mock


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
        # self.assertEqual(self.weapon.images[0], self.weapon.images[-1])
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


class TestMap(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.map = Map(self.game)

    def test_get_map(self):
        self.assertEqual(self.map.world_map, {
            (0, 0): 1,
            (0, 1): 1,
            (0, 2): 1,
            (0, 3): 1,
            (0, 4): 1,
            (0, 5): 1,
            (0, 6): 1,
            (0, 7): 1,
            (0, 8): 1,
            (0, 9): 1,
            (0, 10): 1,
            (0, 11): 1,
            (0, 12): 1,
            (0, 13): 1,
            (0, 14): 1,
            (1, 0): 1,
            (1, 11): 1,
            (1, 14): 1,
            (2, 0): 1,
            (2, 11): 1,
            (2, 14): 1,
            (3, 0): 1,
            (3, 4): 1,
            (3, 7): 1,
            (3, 11): 1,
            (3, 14): 2,
            (4, 0): 1,
            (4, 4): 1,
            (4, 7): 1,
            (4, 11): 1,
            (4, 14): 1,
            (5, 0): 1,
            (5, 4): 1,
            (5, 7): 1,
            (5, 11): 2,
            (5, 14): 1,
            (6, 0): 2,
            (6, 4): 1,
            (6, 5): 2,
            (6, 6): 1,
            (6, 7): 1,
            (6, 14): 1,
            (7, 0): 1,
            (7, 11): 2,
            (7, 14): 1,
            (8, 0): 1,
            (8, 11): 1,
            (8, 14): 1,
            (9, 0): 1,
            (9, 5): 1,
            (9, 11): 1,
            (9, 14): 1,
            (10, 0): 1,
            (10, 5): 2,
            (10, 11): 1,
            (10, 12): 1,
            (10, 13): 1,
            (10, 14): 1,
            (11, 0): 1,
            (11, 5): 1,
            (11, 14): 1,
            (12, 0): 1,
            (12, 14): 1,
            (13, 0): 1,
            (13, 14): 1,
            (14, 0): 1,
            (14, 14): 1,
            (15, 0): 1,
            (15, 1): 1,
            (15, 2): 1,
            (15, 3): 1,
            (15, 4): 1,
            (15, 5): 1,
            (15, 6): 1,
            (15, 7): 1,
            (15, 8): 1,
            (15, 9): 1,
            (15, 10): 1,
            (15, 11): 1,
            (15, 12): 1,
            (15, 13): 1,
            (15, 14): 1
        })


class TestAmmo(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.player.x = 2.5
        self.game.player.y = 3.5
        self.ammo = Ammo(self.game, scale=1, shift=0)

    def test_pick_up_adds_ammo_to_weapon(self):
        self.game.weapons.weapons[0].ammo = 0
        self.game.object_manager.sprites.append(self.ammo)
        self.ammo.pick_up()
        self.assertEqual(self.game.weapons.weapons[0].ammo, 5)

    def test_pick_up_removes_ammo_from_map(self):
        self.ammo.pick_up()
        self.assertNotIn(self.ammo, self.game.object_manager.sprites)


class RayCastingTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()
        self.ray_casting = RayCasting(self.game)

    def test_ray_cast(self):
        self.game.player.angle = 0
        self.ray_casting.ray_cast()
        self.assertEqual(len(self.ray_casting.ray_casting_result), NUM_RAYS)
        self.assertEqual(len(self.ray_casting.ray_casting_result[0]), 4)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][0], float)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][1], float)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][2], int)
        self.assertIsInstance(self.ray_casting.ray_casting_result[0][3], float)
