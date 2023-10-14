from pygame.sprite import Sprite, Group
from pygame.math import Vector2 as V2
from pygame import Surface

from code.utils import load_images_animation


class Player(Sprite):
    def __init__(self, pos: tuple, collision_sprites: Group, *groups) -> None:
        super().__init__(*groups)

        self.animations = {}
        self.animation_speed = 10
        self._import_assets()
        self.frame_index = 0
        self.status = 'up'
        # self.image = self.animation[self.frame_index]
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.pos = V2(self.rect.center)
        self.direction = V2()
        self.speed = 200
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

    def _import_assets(self):
        self.animations = load_images_animation("graphics/player", convert_alpha=True)

    def _move(self, dt: float, keys_lrud: list):
        self.direction.x = keys_lrud[1] - keys_lrud[0]
        self.direction.y = keys_lrud[3] - keys_lrud[2]
        if keys_lrud[0]:
            self.status = 'left'
        if keys_lrud[1]:
            self.status = 'right'
        if keys_lrud[2]:
            self.status = 'up'
        if keys_lrud[3]:
            self.status = 'down'
        if self.direction.magnitude():
            self.direction.normalize()
        
        # horizontal movement
        if self.direction.x:
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.collision('horizontal')

        # vertical movement
        if self.direction.y:
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            self.collision('vertical')

    def animate(self, dt: float):
        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        if direction == 'vertical':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
            
    def update(self, data: dict) -> None:
        self._move(data['dt'], data['keys_lrud'])
        self.animate(data['dt'])
        self.restrict()

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery