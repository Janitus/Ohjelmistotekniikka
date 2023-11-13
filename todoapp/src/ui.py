import pygame

pygame.font.init()

darkgray = (255/8, 255/8, 255/8)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

BAR_WIDTH = 100
font = pygame.font.Font(None, 22)


class UI:
    def __init__(self, player):
        self.player = player

    def draw_health_bar(self, surface):
        x = 10
        y = 10

        hp = self.player.health
        max_hp = self.player.max_health

        health_width = int((hp / max_hp) * 100)
        background_bar = pygame.draw.rect(
            surface, darkgray, (x, y, BAR_WIDTH, 20))
        pygame.draw.rect(surface, red, (x, y, health_width, 20))

        text_surf = font.render(f"{hp} / {max_hp} health", True, white)
        text_rect = text_surf.get_rect(center=background_bar.center)

        surface.blit(text_surf, text_rect)

    def draw_ammo_bar(self, surface):
        x = 10
        y = 35

        ammo = self.player.ammo
        max_ammo = self.player.max_ammo

        ammo_width = int((ammo / max_ammo) * 100)
        background_bar = pygame.draw.rect(
            surface, darkgray, (x, y, BAR_WIDTH, 20))

        pygame.draw.rect(surface, blue, (x, y, ammo_width, 20))

        text_surf = font.render(f"{ammo} / {max_ammo} ammo", True, white)
        text_rect = text_surf.get_rect(center=background_bar.center)

        surface.blit(text_surf, text_rect)

    def draw_money(self, surface):
        x = 10
        y = 60

        money = self.player.money

        text_surf = font.render(f"{money}€", True, white)

        surface.blit(text_surf, (x, y))

    def draw_lives(self, surface):
        x = 10
        y = 85

        lives = self.player.life

        text_surf = font.render(f"{lives} lives", True, white)

        surface.blit(text_surf, (x, y))

    def draw(self, surface):
        self.draw_health_bar(surface)
        self.draw_ammo_bar(surface)
        self.draw_money(surface)
        self.draw_lives(surface)
