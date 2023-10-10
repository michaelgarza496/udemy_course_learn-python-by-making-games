from pygame.sprite import Sprite
from pygame.math import Vector2 as V2
from pygame import Surface

from code.utils import load_images_animation


class Player(Sprite):
    def __init__(self, pos: tuple, *groups) -> None:
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
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def animate(self, dt: float):
        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += self.animation_speed * dt
            if self.frame_index > len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def update(self, dt: float, keys_lrud: list) -> None:
        self._move(dt, keys_lrud)
        self.animate(dt)
