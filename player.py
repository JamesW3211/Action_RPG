import pygame
from pygame.math import Vector2 as vector
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)


    def get_status(self):
        #idle
        if self.direction.x == 0 and self.direction.y ==0:
            self.status = self.status.split('_')[0] + "_idle"

        #attack
        if self.attacking:
            self.status = self.status.split('_')[0] + "_attack"



    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"

            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0

    def animate(self,dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        # if int(self.frame_index) == 1 and self.attacking:
        #     if self.get_player_distance_direction()[0] < self.attack_radius:
        #         self.player.damage()

        self.image = current_animation[int(self.frame_index)]


    def update(self,dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)

        self.vulnerability_timer()