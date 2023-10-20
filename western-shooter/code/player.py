from os import walk
import pygame
from pygame.math import Vector2 as V2
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, pos, groups, path, collision_sprites) -> None:
        super().__init__(*groups)
        # assets
        self.animations = {}
        self.import_assets(path)

        self.frame_index = 0
        self.status = 'down_idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = V2(self.rect.center)
        self.direction = V2()
        self.speed = 200

        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

        # attack
        self.attacking = False

        
    
    def import_assets(self, path):
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []

            else:
                for filename in sorted(folder[2], key=lambda string: string.split('.')[0]):
                    path = folder[0].replace('\\', '/') + '/' + filename
                    surf = pygame.image.load(path).convert_alpha()
                    key = path.split('/')[-2]
                    self.animations[key].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        
        if not self.attacking:
            if self.direction.y:
                self.status = 'down' if self.direction.y > 0 else 'up'
            elif self.direction.x:
                self.status = 'right' if self.direction.x > 0 else 'left'
            elif not self.status.endswith('_idle'):
                self.status = self.status.split('_')[0] + '_idle'
            
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction.x = 0
                self.direction.y = 0
                self.frame_index = 0
        
        # attack
        elif self.attacking:
            self.status = self.status.split('_')[0] + '_attack'
    
    # def get_status(self):
    #     # idle
    #     if not self.attacking and 

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.centerx, self.hitbox.centery = round(self.pos.x), round(self.pos.y)
        self.rect.center = self.hitbox.center
    
    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
