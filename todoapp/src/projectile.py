import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, damage):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(direction)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def check_collision(self, target_group):
        print("todo")