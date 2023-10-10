import pygame
import sys

from code.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from code.utils import create_group
from code.player import Player
from code.car import Car


class Frogger:
    def __init__(self) -> None:
        self._init_pygame()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.all_groups: list = []
        self._init_groups()
        self._init_sprites()
        self.clock = pygame.time.Clock()
        self.keys_lrud = [False, False, False, False]

    def main_loop(self):
        while True:
            self.dt = self.clock.tick() / 1000
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Frogger")

    def _init_groups(self):
        self.player_group = create_group(self.all_groups)
        self.car_group = create_group(self.all_groups)

    def _init_sprites(self):
        self.player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.player_group)
        self.car = Car((100, 100), self.car_group)

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
        self.player_group.update(self.dt, self.keys_lrud)
        self.car_group.update(self.dt)

    def _draw(self):
        self.display_surface.fill("black")
        for group in self.all_groups:
            group.draw(self.display_surface)
        pygame.display.update()
