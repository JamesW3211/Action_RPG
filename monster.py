import pygame
from entity import Entity
from pygame.math import Vector2 as vector

class Monster:
    def get_player_distance_direction(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()
        return (distance, direction)

    def face_player(self):
        distance, direction = self.get_player_distance_direction()

        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:
                    self.status = "left_idle"
                elif direction.x > 0:
                    self.status = "right_idle"
            else:
                if direction.y < 0:
                    self.status = "up_idle"
                elif direction.y > 0:
                    self.status = "down_idle"

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split("_")[0]

        else:
            self.direction = vector()


class Enemy(Entity, Monster):
    def __init__(self, pos, groups, path, collision_sprites, player):
        super().__init__(pos, groups, path, collision_sprites)

        self.speed = 50

        self.player = player
        self.notice_radius = 150
        self.walk_radius = 100
        self.attack_radius = 30
        self.health = 3

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0

        if self.attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self,dt):
        current_animation = self.animations[self.status]


        if int(self.frame_index) == 1 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage()


        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]


    def update(self,dt):

        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move(dt)
        self.animate(dt)
        self.check_death()
        self.vulnerability_timer()












