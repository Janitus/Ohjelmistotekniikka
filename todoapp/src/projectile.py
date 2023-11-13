import pygame
import map


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, source):
        super().__init__()
        self.source = source
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(direction)
        self.speed = 5
        self.damage = 1
        self.knock_power = 1

        self.gravity = 0
        self.y_velocity = 0

    def set_size(self, width, height):
        self.image = pygame.Surface((width, height))

    def set_color(self, r, g, b):
        self.image.fill((int(r), int(g), int(b)))

    def update(self):
        self.y_velocity += self.gravity
        self.y_velocity = min(self.y_velocity, 5)

        self.position += self.direction * self.speed
        self.position.y += self.y_velocity
        self.rect.center = self.position

    def check_collision(self):
        if map.get_collision_by_coordinate(self.position.y, self.position.x):
            return True

        return False

    def draw(self, surface, camera_pos):
        camera_offset_x = int(camera_pos[0])
        camera_offset_y = int(camera_pos[1])
        draw_pos = (self.rect.x - camera_offset_x,
                    self.rect.y - camera_offset_y)

        surface.blit(self.image, draw_pos)
