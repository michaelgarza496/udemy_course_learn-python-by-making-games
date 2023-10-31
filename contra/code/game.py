import pygame, sys, time
from pygame.sprite import AbstractGroup, Group
from pygame.math import Vector2 as V2
from pytmx.util_pygame import load_pygame

from player import Player
from settings import *
from tile import Tile, CollisionTile, MovingPlatform





class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = Group()
        self.platform_sprites = Group()

        # Input
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    platform.direction.y = -platform.direction.y
                    # Top collision
                    if platform.direction.y > 0:
                        platform.rect.top = border.bottom
                    # Bottom collision
                    else:
                        platform.rect.bottom = border.top
                    platform.pos.y = platform.rect.y
            

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')
        
        # Collision tiles
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprites])

        # Tiles
        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surf, LAYERS[layer], self.all_sprites)
        

        # Objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self, [self.all_sprites])
        
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites])
            else:
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)

    def game_loop(self):
        self.setup()
        previous_time = time.time()
        while True:

            # Delta time
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time
            
            # Events
            for event in pygame.event.get():
                # Game quit
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.keys['left'] = True
                    if event.key == pygame.K_RIGHT:
                        self.keys['right'] = True
                    if event.key == pygame.K_UP:
                        self.keys['up'] = True
                    if event.key == pygame.K_DOWN:
                        self.keys['down'] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.keys['left'] = False
                    if event.key == pygame.K_RIGHT:
                        self.keys['right'] = False
                    if event.key == pygame.K_UP:
                        self.keys['up'] = False
                    if event.key == pygame.K_DOWN:
                        self.keys['down'] = False

            # dt = self.clock.tick() / 1000
            # dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            # Updates/Draw
            self.all_sprites.update(dt)
            self.all_sprites.custom_draw(self)
            self.platform_collisions()
            # Display
            pygame.display.flip()


class AllSprites(Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = V2()
    
    def custom_draw(self, game: Game):
        player = game.player
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

if __name__ == '__main__':
    Game().game_loop()



# if event.type == pygame.KEYDOWN:
#                     print(event.key)
#                     print(event.type)
#                     print(pygame.K_a)
#                     d = dict(str(event)[str(event).index('{'):str(event).index('}') + 1])
#                     print(d)
            # print(pygame.key.get_pressed()[pygame.K_ESCAPE])

                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     print(str(event) + '\n')
                #     print(str(event.type) + '\n')
                #     print(str(dir(event)) + '\n')
                #     print(str(dir(event.type)) + '\n')