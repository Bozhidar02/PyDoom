import pygame
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.damage_screen = self.get_texture('resources/textures/damage_screen.png', Res)
        self.game_over_screen = self.get_texture('resources/textures/game_over_screen.png', Res)
        self.victory_screen = self.get_texture('resources/textures/victory.png', Res)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/nums/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

    def draw(self):
        self.draw_skybox()
        self.render_game_objects()
        self.draw_player_health()

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def game_over(self):
        self.screen.blit(self.game_over_screen, (0, 0))

    def victory(self):
        self.screen.blit(self.victory_screen, (0, 0))

    def draw_skybox(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        pygame.draw.rect(self.screen, FLOOR_COLOUR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def player_damage(self):
        self.screen.blit(self.damage_screen, (0, 0))

    def render_game_objects(self):
        obj_list = sorted(self.game.ray_cast.objects_to_render, key = lambda y: y[0], reverse=True)
        for depth, image, pos in obj_list:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png')
        }
