from sprites import *
from npc import *


class ObjectManager:
    def __init__(self, game):
        self.game = game
        self.sprites = []
        self.npcs = []
        self.npc_sprite_path = 'resources/sprites/npcs'
        self.static_sprite_path = 'resources/sprites/static'
        self.animated_sprite_path = 'resources/sprites/animated'
        self.npc_positions = {}
        # sprites
        self.add_sprite(SpriteObject(game))
        self.add_sprite(AnimatedSprites(game))
        self.add_sprite(AnimatedSprites(game, pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprites(game, pos=(14.5, 2.5)))
        # items
        self.add_medkit(MedKit(game))
        self.add_ammo(Ammo(game))
        self.add_armour(Armour(game))
        self.add_armour(Armour(game, pos=(1.5, 12.5)))
        # npcs
        self.add_npc(DemonSoldier(game))
        self.add_npc(DemonSoldier(game, pos=(11.5, 4.5)))
        self.add_npc(CacoDemon(game))
        self.add_npc(CacoDemon(game, pos=(14.5, 10)))
        self.add_npc(PainElemental(game))
        self.add_lost_soul(LostSoul(game, pos=(1, 1)))
        self.npc_num = len(self.npcs)

    def update(self):
        self.npc_positions = {npc.map_position for npc in self.npcs if npc.alive}
        for sprite in self.sprites:
            sprite.update()
        for npc in self.npcs:
            npc.update()

    def add_npc(self, npc):
        self.npcs.append(npc)

    def add_lost_soul(self, lost_soul):
        self.npcs.append(lost_soul)

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def add_medkit(self, medkit):
        self.sprites.append(medkit)

    def add_ammo(self, ammo):
        self.sprites.append(ammo)

    def add_armour(self, armour):
        self.sprites.append(armour)
