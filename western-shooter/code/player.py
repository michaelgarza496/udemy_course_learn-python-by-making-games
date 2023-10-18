from typing import Any
import pygame
from pygame.math import Vector2 as V2
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, pos, groups, path, collision_sprites) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((100, 100))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = V2(self.rect.center)
        self.direction = V2()
        self.speed = 200

        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.centerx, self.hitbox.centery = round(self.pos.x), round(self.pos.y)
        self.rect.center = self.hitbox.center


    def update(self, dt):
        self.input()
        self.move(dt)
    