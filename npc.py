import pygame.time

from sprites import *
from random import randint, random, choice


class NPC(AnimatedSprites):
    def __init__(self, game, path='resources/sprites/npcs/soldier/0.png', pos=(11, 1.5), scale=0.6,
                 shift=0.38, animation_time=180):
        super().__init__(game=game, pos=pos, path=path, scale=scale, shift=shift, animation_time=animation_time)
        self.ray_cast_val = None
        self.idle_images = self.get_images(self.path + '/Idle')
        self.attack_images = self.get_images(self.path + '/Attack')
        self.pain_images = self.get_images(self.path + '/Pain')
        self.walk_images = self.get_images(self.path + '/Walk')
        self.death_images = self.get_images(self.path + '/Death')

        self.attack_dist = 6
        self.speed = 0.03
        self.health = 100
        self.size = 10
        self.damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast = False
        self.frame_count = 0
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.npc_brain()

    def npc_brain(self):
        if self.alive:
            self.ray_cast_val = self.ray_cast_line_of_sight()
            self.is_hit()
            if self.pain:
                self.animate_pain()
            elif self.ray_cast_val:
                self.player_search_trigger = True
                if self.dist <= self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)

        else:
            self.animate_death()

    def is_hit(self):
        if self.ray_cast_val and self.game.player.shot and self.dist <= self.game.weapons.equipped_weapon.range:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapons.equipped_weapon.damage
                self.check_status()

    def check_status(self):
        if self.health <= 0:
            self.alive = False
            self.game.sound.npc_death.play()
            self.game.object_manager.npc_num -= 1

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.take_damage(self.damage)

    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_count < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_count += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def wall_coords(self, x, y):
        return (x, y) not in self.game.map.world_map

    def collision_check(self, dx, dy):
        if self.wall_coords(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.wall_coords(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinder.get_path(self.map_position, self.game.player.map_position)
        next_x, next_y = next_pos
        if next_pos not in self.game.object_manager.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.collision_check(dx, dy)

    @property
    def map_position(self):
        return int(self.x), int(self.y)

    def ray_cast_line_of_sight(self):
        if self.game.player.map_position == self.map_position:
            return True
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        ox, oy = self.game.player.position
        x_map, y_map = self.game.player.map_position
        texture_vert, texture_hor = 1, 1
        ray_angle = self.theta
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
            if tile_hor == self.map_position:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
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
            if tile_vert == self.map_position:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        else:
            return False


class DemonSoldier(NPC):
    def __init__(self, game, path='resources/sprites/npcs/soldier/0.png', pos=(11, 1.5), scale=0.6, shift=0.38,
                 animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CacoDemon(NPC):
    def __init__(self, game, path='resources/sprites/npcs/Caco/0.png', pos=(6.5, 10), scale=0.7, shift=0.27,
                 animation_time=200):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.5
        self.health = 150
        self.damage = 20
        self.speed = 0.07
        self.accuracy = 1


class PainElemental(NPC):
    def __init__(self, game, path='resources/sprites/npcs/PainElemental/0.png', pos=(14.5, 4), scale=0.7, shift=0.27,
                 animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.last_attack_time = 0
        self.current_time = None
        self.attack_dist = 7
        self.health = 150
        self.damage = 20
        self.speed = 0.05
        self.accuracy = 1
        self.attack_cooldown = 5000

    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_count < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_count += 1

    def spawn_position_getter(self, x, y):
        spawn_x, spawn_y = self.map_position
        if self.wall_coords(int(spawn_x + x * self.size), int(spawn_y)):
            spawn_x += x
        if self.wall_coords(int(spawn_x), int(spawn_y + y * self.size)):
            spawn_y += y
        return spawn_x, spawn_y

    def spawn_conflict_denier(self, spawn_position):
        return spawn_position in self.game.object_manager.npc_positions

    def spawn_lost_soul(self, spawn_pos):
        lost_soul = LostSoul(self.game, pos=spawn_pos)
        self.game.object_manager.add_lost_soul(lost_soul)
        print("another one")

    def attack(self):
        current_time = pygame.time.get_ticks()
        if self.animation_trigger and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            self.game.sound.npc_attack.play()
            spawn_positions = self.spawn_position_getter(1, 1), self.spawn_position_getter(-1, -1), \
                              self.spawn_position_getter(1, -1), self.spawn_position_getter(-1, 1), \
                              self.spawn_position_getter(1, 0), self.spawn_position_getter(0, 1), \
                              self.spawn_position_getter(-1, 0), self.spawn_position_getter(0, -1)
            for spawn_position in spawn_positions:
                if self.map_position is not spawn_position and self.spawn_conflict_denier(spawn_position):
                    self.spawn_lost_soul(spawn_position)
                    break


class LostSoul(NPC):
    def __init__(self, game, path='resources/sprites/npcs/LostSoul/0.png', pos=(0, 0), scale=0.3, shift=0.27,
                 animation_time=200):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/Death')
        self.attack_dist = 0.3
        self.health = 10
        self.damage = 10
        self.speed = 0.8
        self.accuracy = 1
        self.allowed_time = 10

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.take_damage(self.damage)
            self.alive = False
            self.health = 0
