import pygame
import sys

from pygame.math import Vector2 as V2
from random import choice, randint

from code.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CAR_STARTING_POSITIONS,
    SIMPLE_OBJECTS,
    LONG_OBJECTS,
)
from code.utils import load_image
from code.player import Player
from code.car import Car
from code.sprite import SimpleSprite, LongSprite


class AllSprites(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.offset = V2()
        self.background = load_image(
            "frogger/graphics/main/map.png", convert_alpha=False
        )
        self.overlay = load_image(
            "frogger/graphics/main/overlay.png", convert_alpha=True
        )

    def customize_draw(self, data: dict):
        player = data["player"]
        surface = data["display_surface"]
        # change offset
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        surface.blit(self.background, -self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            surface.blit(sprite.image, sprite.rect.topleft - self.offset)
            # pygame.draw.rect(data['display_surface'], 'green', sprite.rect)

        surface.blit(self.overlay, -self.offset)


class Frogger:
    def __init__(self) -> None:
        self._init_pygame()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._init_groups()
        self._init_sprites()
        self.clock = pygame.time.Clock()
        self.keys_lrud = [False, False, False, False]
        self.car_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.car_timer, 50)
        self.previous_choices = []
        self.font = pygame.font.Font(None, 50)
        self.text_surf = self.font.render("You won", True, "white")
        self.text_rect = self.text_surf.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )
        self.music = pygame.mixer.Sound("./frogger/audio/music.mp3")
        self.music.play(-1)

    def main_loop(self):
        while True:
            self.dt = self.clock.tick() / 1000
            self.data = dict(
                dt=self.dt,
                keys_lrud=self.keys_lrud,
                display_surface=self.display_surface,
                player=self.player,
            )
            self._handle_input()

            if self.player.pos.y >= 1180:
                self._process_game_logic()
                self._draw()
            else:
                self.display_surface.fill("teal")
                self.display_surface.blit(self.text_surf, self.text_rect)
                pygame.display.update()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Frogger")

    def _init_groups(self):
        # self.player_group = create_group(self.all_sprites)
        # self.car_group = create_group(self.all_sprites)
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        pass

    def _init_sprites(self):
        self.player = Player((2062, 3274), self.collision_sprites, self.all_sprites)

        # simple sprites
        for file_name, pos_list in SIMPLE_OBJECTS.items():
            surf = load_image(f"./graphics/objects/simple/{file_name}.png")
            for pos in pos_list:
                SimpleSprite(surf, pos, self.all_sprites, self.collision_sprites)

        # long sprites
        for file_name, pos_list in LONG_OBJECTS.items():
            surf = load_image(f"./graphics/objects/long/{file_name}.png")
            for pos in pos_list:
                LongSprite(surf, pos, self.all_sprites, self.collision_sprites)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.car_timer:
                random_pos = choice(CAR_STARTING_POSITIONS)
                if random_pos not in self.previous_choices:
                    pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                    Car(pos, self.all_sprites, self.collision_sprites)
                    self.previous_choices.append(random_pos)
                    if len(self.previous_choices) > 5:
                        del self.previous_choices[0]
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
