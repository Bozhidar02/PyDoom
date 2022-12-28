from sprites import *


class Weapon(AnimatedSprites):
    def __init__(self, game, path='resources/sprites/weapons/shotgun/shotgun0.png', scale=0.4,
                 animation_time=90, damage=100, w_range=10):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pygame.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.damage = damage
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.range = w_range

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()


class Shotgun(Weapon):
    def __init__(self, game, path='resources/sprites/weapons/shotgun/shotgun0.png', scale=0.4,
                 animation_time=90, damage=100, w_range=10):
        super().__init__(game, path, scale, animation_time, damage, w_range)


class Chainsaw(Weapon):
    def __init__(self, game, path='resources/sprites/weapons/chainsaw/0.png', scale=4.5,
                 animation_time=70, damage=50, w_range=2):
        super().__init__(game, path, scale, animation_time, damage, w_range)
