import pygame

game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 1],
    [1, False, False, 1, 1, 1, 1, False, False, False, False, False, False, False, False, 1],
    [1, False, False, False, False, False, 1, False, False, 1, 1, 1, False, False, False, 1],
    [1, False, False, False, False, False, 1, False, False, False, False, False, False, False, False, 1],
    [1, False, False, 1, 1, 1, 1, False, False, False, False, False, False, False, False, 1],
    [1, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 1],
    [1, False, False, False, 1, False, False, False, False, False, 1, False, False, False, False, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Map:
    def __init__(self, game):
        self.game = game
        self.game_map = game_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.game_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    # test method
    def test_draw(self):
        [pygame.draw.rect(self.game.screen, 'red', (pos[0] * 100, pos[1]*100, 100, 100), 2)
         for pos in self.world_map]
