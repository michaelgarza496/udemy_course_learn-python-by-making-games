from typing import Any
import pygame

from pygame.math import Vector2 as V2
from settings import *
from pygame import Surface

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf: Surface, z, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=(pos))
        self.z = z
        

class CollisionTile(Tile):
    def __init__(self, pos, surf: Surface, groups) -> None:
        super().__init__(pos, surf, LAYERS['Level'], groups)
        self.prev_rect = self.rect.copy()


class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf: Surface, groups) -> None:
        super().__init__(pos, surf, groups)

        # float based movement
        self.direction = V2(0, -1)
        self.speed = 200
        self.pos = V2(self.rect.topleft)
    
    def update(self, dt) -> None:
        self.prev_rect.topleft = self.rect.topleft
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))