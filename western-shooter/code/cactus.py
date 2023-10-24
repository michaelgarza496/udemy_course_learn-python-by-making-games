import pygame
from entity import Entity

class Cactus(Entity):
    def __init__(self, pos, groups, path, collision_sprites) -> None:
        super().__init__(pos, groups, path, collision_sprites)

        