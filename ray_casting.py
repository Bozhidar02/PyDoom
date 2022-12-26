import pygame
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.position
        x_map, y_map = self.game.player.map_position
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for _ in range(NUM_RAYS):
            sina = math.sin(ray_angle)
            cosa = math.cos(ray_angle)
            # horizontal
            if sina > 0:
                y_hor, dy = (y_map + 1, 1)
            else:
                y_hor, dy = (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sina
            x_hor = ox + depth_hor * cosa
            delta_depth = dy / sina
            dx = delta_depth * cosa
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
            # vertical
            x_vert, dx = (x_map + 1, 1) if cosa > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cosa
            y_vert = oy + depth_vert * sina
            delta_depth = dx / cosa
            dy = delta_depth * sina
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            # depth
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            # test stuff
            pygame.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
                             (100 * ox + 100 * depth * cosa, 100 * oy + 100 * depth * sina), 2)
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
