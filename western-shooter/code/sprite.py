import pygame
from pygame.math import Vector2 as V2

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, surf, groups) -> None:
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = V2(self.rect.center)
        self.direction = direction
        self.speed = 400
    
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
