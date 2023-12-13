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

    def draw_score_screen(self, scores, current_score, color_fill=(20, 20, 20)):
        """Draws a screen displaying the current score and a list of high scores."""
        self.game_window.fill(color_fill)

        font = pygame.font.SysFont("Arial", 20)
        start_y = 80

        current_score_text = f"Your score: {current_score}"
        score_surface = font.render(current_score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.game_resolution[0] / 2, start_y))
        self.game_window.blit(score_surface, score_rect)

        for index, (_, score) in enumerate(scores):
            score_text = f"{index + 1}. {score} points"
            score_surface = font.render(score_text, True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.game_resolution[0] / 2,
                                                        start_y + 25 * (index + 1)))
            self.game_window.blit(score_surface, score_rect)

        pygame.display.flip()

    def draw_score_graph(self, scores,
                         box_color=(255, 255, 255),
                         color=(255, 0, 0),
                         text_color=(255, 255, 255)):
        """Draws a graph based on the scores array."""

        if not scores:
            return

        graph_width = self.game_resolution[0] - 100
        graph_height = self.game_resolution[1] - 400
        graph_x = 50
        graph_y = 400

        max_score = max(scores)

        step = graph_width / (len(scores) - 1)

        font = pygame.font.SysFont("Arial", 12)

        pygame.draw.rect(self.game_window, box_color,
                         (graph_x, graph_y, graph_width, graph_height), 2)

        for i in range(len(scores) - 1):
            y1 = graph_height - (scores[i] / max_score) * graph_height + graph_y
            y2 = graph_height - (scores[i + 1] / max_score) * graph_height + graph_y

            start_pos = (graph_x + i * step, y1)
            end_pos = (graph_x + (i + 1) * step, y2)

            pygame.draw.line(self.game_window, color, start_pos, end_pos, 2)
            pygame.draw.circle(self.game_window, color, (int(start_pos[0]), int(start_pos[1])), 3)

            score_text = font.render(str(scores[i]), True, text_color)
            self.game_window.blit(score_text,
                                  (start_pos[0] - score_text.get_width() / 2, start_pos[1] - 20))

        pygame.draw.circle(self.game_window, color, (int(end_pos[0]), int(end_pos[1])), 3)
        score_text = font.render(str(scores[-1]), True, text_color)
        self.game_window.blit(score_text,
                              (end_pos[0] - score_text.get_width() / 2, end_pos[1] - 20))

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
