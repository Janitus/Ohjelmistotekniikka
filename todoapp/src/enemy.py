import pygame, map
from character import Character

class Enemy(Character):
    def __init__(self, image, pos, width=16, height=24):
        super().__init__(image, pos, width, height)
        self.avoids_falls = True
        self.speed = 0.5
        self.melee_damage = 1
        self.melee_knock = 1.8

    def update(self):
        self.patrol()
        super().update()

    def die(self):
        self.dead = True

    def patrol(self):
        if (self.avoids_falls and self.is_facing_a_fall()): self.direction.x *= -1

        if (not self.collides(self.direction.x * self.speed, 0)):
            self.move(self.direction.x * self.speed, 0)
        else:
            self.direction.x *= -1

    def is_facing_a_fall(self):
        if  (self.direction.x > 0   and map.get_collision_by_coordinate(self.position.y+10,self.position.x+self.speed) == True): return False
        elif (self.direction.x <= 0 and map.get_collision_by_coordinate(self.position.y+10,self.position.x-self.speed) == True): return False

        return True

    def draw(self, surface, camera_pos):
        super().draw(surface, camera_pos)