from settings import *
import pygame
import math


class Player:
    def __init__(self, game):
        self.rel = None
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE

    def movement(self):
        sina = math.sin(self.angle)
        cosa = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta
        speed_sin = sina * speed
        speed_cos = cosa * speed
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
        scale = PLATER_SIZE / self.game.delta
        if self.wall_coords(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.wall_coords(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_look(self):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta

    def update(self):
        self.movement()
        self.mouse_look()

    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)
