import pygame
from pygame.math import Vector2 as V2
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet) -> None:
        super().__init__(pos, groups, path, collision_sprites)
        # attack
        self.create_bullet = create_bullet
        self.bullet_shot = False
        self.bullet_direction = None       
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        
        # move or idle
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
                self.bullet_shot = False

                match self.status.split('_')[0]:
                    case 'left': self.bullet_direction = V2(-1, 0)
                    case 'right': self.bullet_direction = V2(1, 0)
                    case 'up': self.bullet_direction = V2(0, -1)
                    case 'down': self.bullet_direction = V2(0, 1)
        
        # attack
        elif self.attacking:
            self.status = self.status.split('_')[0] + '_attack'
  
    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * dt

        if self.attacking and int(self.frame_index) == 2 and not self.bullet_shot:
            bullet_start_pos = self.rect.center + self.bullet_direction * 80
            self.create_bullet(bullet_start_pos, self.bullet_direction)
            self.bullet_shot = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]     

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)




        # if self.direction:
        #     for sprite in self.collision_sprites:
        #         if sprite.hitbox.colliderect(self.hitbox):
        #             if self.direction.x > 0:
        #                 self.hitbox.right = sprite.hitbox.left
        #             elif self.direction.x < 0:
        #                 self.hitbox.left = sprite.hitbox.right
        #             if self.direction.y > 0:
        #                 self.hitbox.bottom = sprite.hitbox.top
        #             elif self.direction.y < 0:
        #                 self.hitbox.top = sprite.hitbox.bottom
        #             self.rect.center = self.hitbox.center
        #             self.pos.x, self.pos.y = self.hitbox.centerx, self.hitbox.centery  