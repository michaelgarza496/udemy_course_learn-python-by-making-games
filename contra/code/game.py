import pygame, sys
from pygame.sprite import Group
from pytmx.util_pygame import load_pygame

from settings import *
from tile import Tile


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = Group()
        self.setup()
    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            Tile((x * 64, y * 64), surf, self.all_sprites)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
            
            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            # Updates/Draw
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            # Display
            pygame.display.update()

if __name__ == '__main__':
    Game().game_loop()



# if event.type == pygame.KEYDOWN:
#                     print(event.key)
#                     print(event.type)
#                     print(pygame.K_a)
#                     d = dict(str(event)[str(event).index('{'):str(event).index('}') + 1])
#                     print(d)
            # print(pygame.key.get_pressed()[pygame.K_ESCAPE])