import pygame, sys
from pygame.sprite import Group
from pygame.math import Vector2 as V2
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet

from player import Player
from coffin import Coffin
from cactus import Cactus
from settings import *


class AllSprites(Group):
    def __init__(self) -> None:
        super().__init__()
        self.offset = V2()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('../graphics/other/bg.png').convert()
    
    def customized_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2


        self.display_surface.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Game:
    def __init__(self) -> None:
        # init stuff
        pygame.init()
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Western Shooter")
        # time
        self.clock = pygame.time.Clock()
        # groups
        self.all_sprites = AllSprites()
        self.obstacles = Group()
        self.bullets = Group()

        self.bullet_surf = pygame.image.load('../graphics/other/particle.png').convert_alpha()
        self.setup()

    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')

        # fence
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            tile_width = surf.get_width()
            tile_height = surf.get_height()
            pos = (x * tile_width, y * tile_height)
            Sprite(pos, surf, [self.all_sprites, self.obstacles])
        
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Sprite((obj.x, obj.y), self.display_surf, self.all_sprites) #This has cool effects
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])
        
        # entities
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    groups=[self.all_sprites], 
                    path=PATHS['player'], 
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet)
            if obj.name == 'Coffin':
                Coffin(
                    pos=(obj.x, obj.y), 
                    groups=[self.all_sprites], 
                    path=PATHS['coffin'], 
                    collision_sprites=self.obstacles,
                    player=self.player)
            if obj.name == 'Cactus':
                Cactus(
                    pos=(obj.x, obj.y), 
                    groups=[self.all_sprites], 
                    path=PATHS['cactus'], 
                    collision_sprites=self.obstacles)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surf.fill("black")
            dt = self.clock.tick() / 1000

            # update groups
            self.all_sprites.update(dt)

            # draw groups
            self.all_sprites.customized_draw(self.player)

            pygame.display.update()


if __name__ == "__main__":
    Game().run()
