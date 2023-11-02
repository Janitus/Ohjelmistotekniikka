import pygame
from character import Character

class Player(Character):
    def __init__(self, image, pos, width, height):
        super().__init__(image, pos, width, height)

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
    def draw(self, surface, camera_pos):
        super().draw(surface, camera_pos)

        #surface.blit(self.image, (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1]))
        #surface.blit(self.image, self.rect)
