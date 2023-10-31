import pygame, os
from pygame import Vector2 as V2
from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, game, groups) -> None:
        super().__init__(groups)
        # Animations
        self.animations = {}
        self.import_assets(ASSETS_PATH['player'])
        self.frame_index = 0
        self.status = 'right'
        self.starting_pos = pos

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=self.starting_pos)
        
        # Input
        self.keys = game.keys

        # Position, , Direction, Speed
        self.z = LAYERS['Level']
        self.pos = V2(self.rect.topleft)
        self.direction = V2()
        self.speed = 500

        # Collision
        self.prev_rect = self.rect.copy()
        self.collision_sprites: Group = game.collision_sprites
        self.moving_floor = None

        # Vertical movement
        self.gravity = 15
        self.jump_speed = 1400
        self.on_floor = False
        self.ducking = False

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                
                if direction == 'horizontal':
                    # Left collison
                    if self.rect.left <= sprite.rect.right and self.prev_rect.left >= sprite.prev_rect.right:
                        self.rect.left = sprite.rect.right
                    # Right collison
                    elif self.rect.right >= sprite.rect.left and self.prev_rect.right <= sprite.prev_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x
                elif direction == 'vertical':
                    # Up collison
                    if self.rect.top <= sprite.rect.bottom and self.prev_rect.top >= sprite.prev_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # Down collison
                    elif self.rect.bottom >= sprite.rect.top and self.prev_rect.bottom <= sprite.prev_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False
    
    def import_assets(self, path_to_animations):
        for i, files in enumerate(os.walk(path_to_animations)):
            if i == 0:
                self.animations = {state: None for state in files[1]}
            else:
                path = files[0].replace('\\', '/')
                state = path.split('/')[-1]
                surfaces = [pygame.image.load(path + '/' + f).convert_alpha() 
                            for f in sorted(files[2], key=lambda file: int(file.split('.')[0]))]
                self.animations[state] = surfaces

    def get_status(self):
        #idle
        if not self.direction.x and self.on_floor: 
            self.status = self.status.split('_')[0] + '_idle'
        
        # jump
        elif not self.on_floor and self.direction.y:
            self.status = self.status.split('_')[0] + '_jump'

        # duck
        if self.on_floor and self.ducking:
            self.status = self.status.split('_')[0] + '_duck'
        
    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite, 'direction'):
                    self.moving_floor = sprite
                break

    def input(self):
        self.direction.x = self.keys['right'] - self.keys['left']
        if self.direction.x:
            self.status = 'right' if self.direction.x > 0 else 'left'
        # if self.direction.x == 0 and '_idle' not in self.status:
        #     self.status += '_idle'
        # else:
        #     self.status = 'right' if self.direction.x > 0 else 'left'
        # self.direction.y = self.keys['down'] - self.keys['up']
        if self.keys['up'] and self.on_floor:
            self.direction.y = -self.jump_speed
        
        if self.keys['down']:
            self.ducking = True
        else:
            self.ducking = False

    def move(self, dt):
        if self.on_floor and self.ducking:
            self.direction.x = 0
        
        # Horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # Vertical
        self.direction.y = min(self.direction.y + self.gravity, self.speed * 3)
        self.pos.y += self.direction.y * dt

        # Glue the player to the moving platform
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.moving_floor = None

    def animate(self,dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self, dt):
        self.prev_rect.topleft = self.rect.topleft
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
        # print(self.direction, self.direction.magnitude())
