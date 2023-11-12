import pygame
import pytmx
from projectile_manager import ProjectileManager

class Renderer:
    def __init__(self, game_surface, game_window, game_resolution, zoomed_resolution):
        self.game_surface = game_surface
        self.tmx_level = None
        self.game_window = game_window
        self.game_resolution = game_resolution
        self.zoomed_resolution = zoomed_resolution
        self.zoom_amount = 1

    def handle_rendering(self, player, ui, lighting, camera_pos, pickups, enemies, projectile_manager: ProjectileManager):
        self.game_surface.fill((40, 40, 40))

        if(self.tmx_level != None): self.draw_map(camera_pos)
        player.draw(self.game_surface, camera_pos)

        for enemy in enemies:enemy.draw(self.game_surface, camera_pos)
        for pickup in pickups: pickup.draw(self.game_surface, camera_pos)
        projectile_manager.draw(self.game_surface, camera_pos)

        lighting.draw(self.game_surface, camera_pos)

        offset_x = (player.rect.centerx - camera_pos[0]) * self.zoom_amount - self.game_resolution[0] // 2
        offset_y = (player.rect.centery - camera_pos[1]) * self.zoom_amount - self.game_resolution[1] // 2

        scaled_surface = pygame.transform.scale(self.game_surface, self.zoomed_resolution)
        self.game_window.blit(scaled_surface, (-offset_x, -offset_y))

        ui.draw(self.game_window)

        pygame.display.flip()

    def draw_message_screen (self, message="Loading next level", color_fill = (20,20,20)):
        self.game_window.fill(color_fill)

        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.game_resolution[0] / 2, self.game_resolution[1] / 2))

        self.game_window.blit(text_surface, text_rect)

        pygame.display.flip()

    def draw_map(self, camera_pos):
        tw = self.tmx_level.tilewidth
        th = self.tmx_level.tileheight
        for layer in self.tmx_level.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_level.get_tile_image_by_gid(gid)
                    if tile:
                        tile_x = (x * tw) - camera_pos[0]
                        tile_y = (y * th) - camera_pos[1]
                        self.game_surface.blit(tile, (tile_x, tile_y))
