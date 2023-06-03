"""
Action RPG
Created by JamesW
This file was created with the purpose of learning the basics of Python programing

"""


import pygame, sys
from settings import *
from pygame.math import Vector2 as vector
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load("graphics/other/bg.png").convert_alpha()

    def customize_draw(self, player):

        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        self.display_surface.blit(self.bg,(-self.offset))
        for sprite in sorted(self.sprites(), key = lambda sprite:sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image,offset_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("RPG")
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()

        self.setup()

    def setup(self):
        tmx_map = load_pygame("data/map.tmx")
        # for x, y, surf in tmx_map.get_layer_by_name("Tree").tiles():
        #     Sprite((x * 64,y * 64),surf,self.all_sprites )

        for obj in tmx_map.get_layer_by_name("Objects"):
            Sprite((obj.x, obj.y),obj.image ,[self.all_sprites, self.obstacles])



        self.player = Player((220,120), self.all_sprites, Paths["player"], self.obstacles)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000


            self.all_sprites.update(dt)

            self.display_surface.fill("black")


            self.all_sprites.customize_draw(self.player)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()


