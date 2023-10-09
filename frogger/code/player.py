from pygame.sprite import Sprite
from pygame.math import Vector2 as V2
from pygame import Surface

from code.utils import load_images


class Player(Sprite):
    def __init__(self, pos: tuple, *groups) -> None:
        super().__init__(*groups)
        self.image = Surface((50, 50))
        self.rect = self.image.get_rect(center=pos)
        self.image.fill("red")
        self._import_assets()
        self.pos = V2(self.rect.center)
        self.direction = V2()
        self.speed = 200

    def _import_assets(self):
        self._animation = load_images("player/left", in_range=3)
        print(self._animation)

    def _move(self, dt: float, keys_lrud: list):
        self.direction.x = keys_lrud[1] - keys_lrud[0]
        self.direction.y = keys_lrud[3] - keys_lrud[2]
        if self.direction.magnitude():
            self.direction.normalize()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, keys_lrud: list) -> None:
        self._move(dt, keys_lrud)
