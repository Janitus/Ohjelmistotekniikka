import pygame

pygame.font.init()

# Health
darkgray = (255/8, 255/8, 255/8)
red = (255, 0, 0)
white = (255, 255, 255)
health_bar_width = 100
health_font = pygame.font.Font(None, 24)

class UI:
    def __init__(self, player):
        self.player = player

    def draw_health_bar(self, surface):
        x = 10
        y = 10

        hp = self.player.health
        max_hp = self.player.max_health

        health_width = int((hp / max_hp) * 100)
        background_bar = pygame.draw.rect(surface, darkgray, (x, y, health_bar_width, 20))
        pygame.draw.rect(surface, red, (x, y, health_width, 20))

        text_surf = health_font.render(f"{hp} / {max_hp}", True, white)
        text_rect = text_surf.get_rect(center=background_bar.center)

        surface.blit(text_surf, text_rect)
    def draw(self, surface):
        self.draw_health_bar(surface)