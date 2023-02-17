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
        self.add_sprite(AnimatedSprites(game, pos=(4.5, 1.5)))
        self.add_sprite(AnimatedSprites(game, pos=(14.5, 3.5)))
        self.add_sprite(AnimatedSprites(game, pos=(6.5, 20.5)))
        # items
        self.add_medkit(MedKit(game, pos=(11.5, 1.5)))
        self.add_medkit(MedKit(game, pos=(11.5, 2.5)))
        self.add_medkit(MedKit(game, pos=(2.5, 4.4)))
        self.add_medkit(MedKit(game, pos=(1.5, 6.4)))
        self.add_medkit(MedKit(game, pos=(2.5, 19.5)))
        self.add_medkit(MedKit(game, pos=(2.5, 20.5)))
        self.add_ammo(Ammo(game, pos=(13.5, 2.5)))
        self.add_ammo(Ammo(game, pos=(13.5, 1.5)))
        self.add_ammo(Ammo(game, pos=(11.5, 7.5)))
        self.add_ammo(Ammo(game, pos=(1.5, 8.5)))
        self.add_ammo(Ammo(game, pos=(4.5, 20.5)))
        self.add_ammo(Ammo(game, pos=(4.5, 19.5)))
        self.add_ammo(Ammo(game, pos=(15.5, 20.5)))
        self.add_armour(Armour(game))
        self.add_armour(Armour(game, pos=(1.5, 12.5)))
        self.add_armour(Armour(game, pos=(11.5, 19.5)))
        self.add_armour(Armour(game, pos=(11.5, 18.5)))
        self.add_armour(Armour(game, pos=(1.5, 20.5)))
        self.add_armour(Armour(game, pos=(1.5, 19.5)))
        # npcs
        self.add_npc(DemonSoldier(game, pos=(7.5, 2)))
        self.add_npc(DemonSoldier(game, pos=(15.9, 11.4)))
        self.add_npc(DemonSoldier(game, pos=(2.5, 16.5)))
        self.add_npc(DemonSoldier(game, pos=(9.5, 17.5)))
        self.add_npc(DemonSoldier(game, pos=(11.5, 4.5)))
        self.add_npc(DemonSoldier(game, pos=(12.5, 4.5)))
        self.add_npc(DemonSoldier(game, pos=(24.5, 16.5)))
        self.add_npc(DemonSoldier(game, pos=(19.5, 20.5)))
        self.add_npc(CacoDemon(game, pos=(7.5, 3)))
        self.add_npc(CacoDemon(game, pos=(2, 9.5)))
        self.add_npc(CacoDemon(game, pos=(24.5, 8)))
        self.add_npc(CacoDemon(game, pos=(24.5, 3)))
        self.add_npc(CacoDemon(game, pos=(24.5, 19.5)))
        self.add_npc(PainElemental(game,  pos=(24.5, 3)))
        self.add_npc(PainElemental(game,  pos=(8.5, 19.5)))
        self.npc_num = len(self.npcs)

    def update(self):
        self.npc_positions = {npc.map_position for npc in self.npcs if npc.alive}
        for sprite in self.sprites:
            sprite.update()
        for npc in self.npcs:
            npc.update()
        self.victory_check()

    def victory_check(self):
        if not len(self.npc_positions):
            self.game.obj_render.victory()
            pygame.display.flip()
            pygame.time.delay(4500)
            self.game.new_game()

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
