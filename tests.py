import unittest
from main import *


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

