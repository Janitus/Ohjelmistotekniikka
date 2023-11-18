"""Renderer that handles rendering everything onto the game window"""
import pygame
import pytmx


class Renderer:
    """Renders everything in the game"""
    def __init__(self, game_surface, game_window, game_resolution, zoomed_resolution):
        self.game_surface = game_surface
        self.game_window = game_window
        self.game_resolution = game_resolution
        self.zoomed_resolution = zoomed_resolution
        self.zoom_amount = 1
        self.game_state = None

    def handle_rendering(self, ui, camera_pos):
        """Takes everything renderable as input and renders them"""
        self.game_surface.fill((40, 40, 40))

        if self.game_state.tmx_level is not None:
            self.draw_map(camera_pos)

        for pickup in self.game_state.pickups:
            pickup.draw(self.game_surface, camera_pos)

        self.game_state.player.draw(self.game_surface, camera_pos)

        for enemy in self.game_state.enemies:
            enemy.draw(self.game_surface, camera_pos)

        self.game_state.projectile_manager.draw(self.game_surface, camera_pos)

        self.game_state.lighting.draw(self.game_surface, camera_pos)

        offset_x = (self.game_state.player.rect.centerx -
                    camera_pos[0]) * self.zoom_amount - self.game_resolution[0] // 2
        offset_y = (self.game_state.player.rect.centery -
                    camera_pos[1]) * self.zoom_amount - self.game_resolution[1] // 2

        scaled_surface = pygame.transform.scale(
            self.game_surface, self.zoomed_resolution)
        self.game_window.blit(scaled_surface, (-offset_x, -offset_y))

        ui.draw(self.game_window)

        pygame.display.flip()

    def draw_message_screen(self, message="Loading next level", color_fill=(20, 20, 20)):
        """Creates a message screen with a message."""
        self.game_window.fill(color_fill)

        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(self.game_resolution[0] / 2, self.game_resolution[1] / 2))

        self.game_window.blit(text_surface, text_rect)

        pygame.display.flip()

    def draw_map(self, camera_pos):
        """Renders the tiled map"""
        for layer in self.game_state.tmx_level.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.draw_tile(layer,camera_pos)

    def draw_tile(self, layer, camera_pos):
        tw = self.game_state.tmx_level.tilewidth
        th = self.game_state.tmx_level.tileheight
        for x, y, gid in layer:
            tile = self.game_state.tmx_level.get_tile_image_by_gid(gid)
            if tile:
                tile_x = (x * tw) - camera_pos[0]
                tile_y = (y * th) - camera_pos[1]
                self.game_surface.blit(tile, (tile_x, tile_y))
