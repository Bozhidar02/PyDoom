from sprites import *
from npc import *


class ObjectManager:
    def __init__(self, game):
        self.game = game
        self.sprites = []
        self.npcs = []
        # sprites
        self.npc_sprite_path = 'resources/sprites/npcs'
        self.static_sprite_path = 'resources/sprites/static'
        self.animated_sprite_path = 'resources/sprites/animated'
        self.npc_positions = {}
        # sprites
        self.add_sprite(SpriteObject(game))
        self.add_sprite(AnimatedSprites(game))
        self.add_sprite(AnimatedSprites(game, pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprites(game, pos=(14.5, 1.5)))
        # npcs
        self.add_npc(NPC(game))
        self.add_npc(NPC(game, pos=(11.5, 4.5)))

    def update(self):
        self.npc_positions = {npc.map_position for npc in self.npcs if npc.alive}
        for sprite in self.sprites:
            sprite.update()
        for npc in self.npcs:
            npc.update()

    def add_npc(self, npc):
        self.npcs.append(npc)

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
