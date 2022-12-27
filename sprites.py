import pygame
from settings import *


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static/candlebra.png', pos=(11, 4.5), scale=0.7, shift=0.27):
        self.sprite_half_width = 0
        self.norm_dist = 1
        self.dist = 1
        self.screen_x = 0
        self.theta = 0
        self.dy = 0
        self.dx = 0
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite(self):
        self.dx = self.x - self.player.x
        self.dy = self.y - self.player.y
        self.theta = math.atan2(self.dy, self.dx)

        delta = self.theta - self.player.angle
        if (self.dx > 0 and self.player.angle > math.pi) or (self.dx < 0 and self.dy < 0):
            delta += math.tau
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        self.dist = math.hypot(self.dx, self.dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_proj()

    def update(self):
        self.get_sprite()

    def get_sprite_proj(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        image = pygame.transform.scale(self.image, (proj_width, proj_height))
        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        self.game.ray_cast.objects_to_render.append((self.norm_dist, image, pos))




