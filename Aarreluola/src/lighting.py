"""Handles lighting based on information in tiled maps"""
import pygame
import pygame.gfxdraw
import pytmx
# pylint: disable=no-member,c-extension-no-member
# Pylint herjaa pygamen jokaisesta ominaisuudesta no-member, joten kytkemme sen pois

class Lighting:
    """Handles the lighting of the game map."""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.darkness = pygame.Surface((screen_width, screen_height))
        self.light_sources = []
        self.torchlight = self.create_light_source(
            (screen_width/2, screen_height/2), 150)
        self.darkness_color = (128, 128, 128)

    def create_light_source(self, position, radius, input_color=(255, 255, 255)):
        """Creates a light source in a fixed location"""
        r = input_color[0]
        g = input_color[1]
        b = input_color[2]

        # Generated
        light = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        for i in range(radius, 0, -1):
            alpha = (1 - (i / radius)) ** 3 * 255
            color = (r, g, b, int(alpha))
            pygame.gfxdraw.filled_circle(light, radius, radius, i, color)
        # End Generated
        return (light, position)

    def add_light_source(self, position, radius, color=(255, 255, 255)):
        """Creates a light source in a fixed location."""
        if isinstance(color, pygame.Color):
            color = (color.r, color.g, color.b, color.a)
        self.light_sources.append(
            self.create_light_source(position, radius, color))

    def update_light_sources(self, new_positions):
        """Updates the positions of the light"""
        for i, (light, _) in enumerate(self.light_sources):
            self.light_sources[i] = (light, new_positions[i])

    def draw(self, screen, camera_pos):
        """Draws the lights"""
        max_dark_surface = pygame.Surface(
            (self.screen_width, self.screen_height))
        max_dark_surface.fill((255, 255, 255))
        self.darkness.fill(self.darkness_color)

        for light, world_position in self.light_sources:
            screen_position = (
                world_position[0] - camera_pos[0], world_position[1] - camera_pos[1])
            self.darkness.blit(light,
                               (screen_position[0] - light.get_width() // 2,
                                screen_position[1] - light.get_height() // 2),
                               special_flags=pygame.BLEND_RGBA_ADD)

        # Torchlight is the light player uses
        torchlight_surface, _ = self.torchlight
        torchlight_position = (self.screen_width // 2 - torchlight_surface.get_width() // 2,
                               self.screen_height // 2 - torchlight_surface.get_height() // 2)
        self.darkness.blit(torchlight_surface,
                           torchlight_position,
                           special_flags=pygame.BLEND_RGBA_ADD)

        self.darkness.blit(max_dark_surface, (0, 0),
                           special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(self.darkness, (0, 0),
                    special_flags=pygame.BLEND_RGBA_MULT)

    def converted_color(self, color):
        """Converts the color from tiled color format, to match the more standard RRGGBBAA"""
        color = pygame.Color(color)
        color = (color.g, color.b, color.a, color.r)
        return color

    def load_lights_from_map(self, tmx_data):
        """Loads the lights from the map file"""
        map_darkness = tmx_data.properties.get('darkness', None)
        if map_darkness is not None:
            self.darkness_color = self.converted_color(map_darkness)

        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                self.create_light_instance_if_valid(layer)

    def create_light_instance_if_valid(self, layer):
        for obj in layer:
            if obj.name == "light":
                posx, posy = obj.x, obj.y
                radius = int(obj.properties.get("radius", 100))
                color = obj.properties.get("color", "#ffffff")
                self.add_light_source(
                    (posx, posy), radius, self.converted_color(color))
