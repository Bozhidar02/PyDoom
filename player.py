from settings import *
import pygame
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta
        speed_sin = sin_a * speed
        speed_cos = cos_a * speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pygame.K_a]:
            dx += speed_sin
            dy += -speed_cos
        self.collision_check(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED * self.game.delta
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED * self.game.delta
        self.angle %= math.tau

    def wall_coords(self, x, y):
        return (x, y) not in self.game.map.world_map

    def collision_check(self, dx, dy):
        if self.wall_coords(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.wall_coords(int(self.x), int(self.y + dy)):
            self.y += dy

    def test_draw(self):
        pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                         (self.x * 100 + WIDTH * math.cos(self.angle),
                          self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)
