import pygame
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.obj_render.wall_textures

    def render_objects(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.position
        x_map, y_map = self.game.player.map_position
        texture_vert, texture_hor = 1, 1
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
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
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
            # vertical
            if cosa > 0:
                x_vert, dx = (x_map + 1, 1)
            else:
                x_vert, dx = (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cosa
            y_vert = oy + depth_vert * sina
            delta_depth = dx / cosa
            dy = delta_depth * sina
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            # depth
            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                offset = y_vert if cosa > 0 else (1 - y_vert)
            else:
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                offset = 1 - x_hor if sina > 0 else x_hor
            # remove fishbow
            depth *= math.cos(self.game.player.angle - ray_angle)
            # projection
            colour = [225 / (1 + depth ** 5 * 0.00002)] * 3
            projection_height = SCREEN_DIST / (depth + 0.0001)

            #ray casting results
            self.ray_casting_result.append((depth, projection_height, texture, offset))
            # test stuff
            # pygame.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
            #                 (100 * ox + 100 * depth * cosa, 100 * oy + 100 * depth * sina), 2)
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.render_objects()
