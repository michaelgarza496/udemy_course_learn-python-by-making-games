import pygame
import sys
from code.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Frogger:
    def __init__(self) -> None:
        self._init_pygame()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
    
    def main_loop(self):
        while True:
            dt =  self.clock.tick() / 1000
            self._handle_input()
            self._process_game_logic()
            self._draw()
    
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Frogger")
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _process_game_logic(self):
        pass

    def _draw(self):
        pygame.display.update()
    