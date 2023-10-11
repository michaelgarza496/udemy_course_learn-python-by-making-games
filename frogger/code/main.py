import pygame
import sys

from pygame.math import Vector2 as V2

from code.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from code.utils import load_image
from code.player import Player
from code.car import Car

class AllSprites(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.offset = V2()
        self.background = load_image('frogger/graphics/main/map.png', convert_alpha=False)
        
    
    def customize_draw(self, data: dict):
        data['display_surface'].blit(self.background, (0, 0))
        for sprite in self.sprites():
            data['display_surface'].blit(sprite.image, sprite.rect.topleft + self.offset)
            # pygame.draw.rect(data['display_surface'], 'green', sprite.rect)

    
    
class Frogger:
    def __init__(self) -> None:
        self._init_pygame()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.all_sprites = AllSprites()
        self._init_groups()
        self._init_sprites()
        self.clock = pygame.time.Clock()
        self.keys_lrud = [False, False, False, False]

    def main_loop(self):
        while True:
            self.dt = self.clock.tick() / 1000
            self.data = dict(dt=self.dt, keys_lrud=self.keys_lrud, display_surface=self.display_surface)
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Frogger")

    def _init_groups(self):
        # self.player_group = create_group(self.all_sprites)
        # self.car_group = create_group(self.all_sprites)
        pass

    def _init_sprites(self):
        self.player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.all_sprites)
        self.car = Car((WINDOW_WIDTH, 100), self.all_sprites)
        self.car2 = Car((0, 400), self.all_sprites)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    self.keys_lrud[0] = True
                if event.key == pygame.K_RIGHT:
                    self.keys_lrud[1] = True
                if event.key == pygame.K_UP:
                    self.keys_lrud[2] = True
                if event.key == pygame.K_DOWN:
                    self.keys_lrud[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keys_lrud[0] = False
                if event.key == pygame.K_RIGHT:
                    self.keys_lrud[1] = False
                if event.key == pygame.K_UP:
                    self.keys_lrud[2] = False
                if event.key == pygame.K_DOWN:
                    self.keys_lrud[3] = False

    def _process_game_logic(self):
        # self.player_group.update(self.dt, self.keys_lrud)
        # self.car_group.update(self.dt)
        self.all_sprites.update(self.data)

    def _draw(self):
        self.display_surface.fill("black")
        # for group in self.all_groups:
        #     group.draw(self.display_surface)
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.customize_draw(self.data)
        pygame.display.update()
