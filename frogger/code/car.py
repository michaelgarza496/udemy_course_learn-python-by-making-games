from random import choice
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2
from pygame.transform import flip

from code.utils import get_random_image

class Car(Sprite):
    def __init__(self, pos: tuple, *groups) -> None:
        super().__init__(*groups)
        self.image = get_random_image('graphics/cars', True)
        self.rect = self.image.get_rect(center = pos)

        # float movement
        self.pos = V2(self.rect.center)
        self.direction = V2()
        self.speed = 300
        self._orient_image()
    
    def _orient_image(self):
        if self.pos.x > 200:
            self.image = flip(self.image, True, False)
            self.direction.x = -1
        else:
            self.direction.x = 1
            

    def update(self, data: dict):
        self.pos += self.direction * self.speed * data['dt']
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not -500 < self.rect.x < 3000:
            self.kill()
        