import pygame
from character import Character

class Player(Character):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        # Add any player-specific initialization here

    def update(self, keys):
        super().update()  # Call the base class update
        # Player-specific update logic
        if keys[pygame.K_w]:
            self.move(0, -self.speed)
        if keys[pygame.K_s]:
            self.move(0, self.speed)
        if keys[pygame.K_a]:
            self.move(-self.speed, 0)
        if keys[pygame.K_d]:
            self.move(self.speed, 0)
    def draw(self, surface, camera_pos):
        super().draw(surface, camera_pos)

        #surface.blit(self.image, (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1]))
        #surface.blit(self.image, self.rect)
