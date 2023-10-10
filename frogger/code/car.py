from random import choice
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2

from code.utils import get_random_image

class Car(Sprite):
    def __init__(self, pos: tuple, *groups) -> None:
        super().__init__(*groups)
        self.image = get_random_image('graphics/cars', True)
        self.rect = self.image.get_rect(center = pos)

        # float movement
        self.pos = V2(self.rect.center)
        self.direction = V2(1, 0)
        self.speed = 300
    
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        