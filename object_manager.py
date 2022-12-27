from sprites import *


class ObjectManager:
    def __init__(self, game):
        self.game = game
        self.sprites = []
        self.static_sprite_path = 'resources/sprites/static'
        self.animated_sprite_path = 'resources/sprites/animated'

        self.add_sprite(SpriteObject(game))
        self.add_sprite(AnimatedSprites(game))

    def update(self):
        [sprite.update() for sprite in self.sprites]

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
