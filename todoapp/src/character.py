import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity_y = 0
        self.speed = 3
        self.hp = 10
        self.gravity = 0.01

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self.apply_gravity()

    def draw(self, surface, camera_pos):
        adjusted_x = self.rect.x - camera_pos[0]
        adjusted_y = self.rect.y - camera_pos[1]
        surface.blit(self.image, (adjusted_x, adjusted_y))
