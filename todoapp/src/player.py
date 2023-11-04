import pygame
from character import Character

class Player(Character):
    def __init__(self, image, pos, width, height):
        super().__init__(image, pos, width, height)
        self.money = 0
        self.life = 3
        self.ammo = 4
        self.max_ammo = 4
        self.keys = set()

    def update(self, keys):
        super().update()
        if keys[pygame.K_w]:
            self.moveUpwards()
        if keys[pygame.K_s]:
            self.moveDownwards()
        if keys[pygame.K_a]:
            self.move(-self.speed, 0)
        if keys[pygame.K_d]:
            self.move(self.speed, 0)

    def receive_key (self, key_name):
        self.keys.add(key_name)
        print(key_name)

    def receive_ammo(self, amount):
        if(amount <= 0): return
        self.ammo += amount
        self.ammo = min(self.ammo,self.max_ammo)

    def draw(self, surface, camera_pos):
        super().draw(surface, camera_pos)

        #surface.blit(self.image, (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1]))
        #surface.blit(self.image, self.rect)
