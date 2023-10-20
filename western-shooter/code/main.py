import pygame, sys
from pygame.sprite import Group

from player import Player
from settings import *


class Game:
    def __init__(self) -> None:
        # init stuff
        pygame.init()
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Western Shooter")
        # time
        self.clock = pygame.time.Clock()
        # groups
        self.all_sprites = Group()

        self.setup()

    def setup(self):
        Player((200, 200), [self.all_sprites], PATHS['player'], None)

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
            self.all_sprites.draw(self.display_surf)

            pygame.display.update()


if __name__ == "__main__":
    Game().run()
