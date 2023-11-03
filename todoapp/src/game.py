import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from ui import UI
from lighting import Lighting
import map

pygame.init()
pygame.display.set_caption ("Placeholder Name")

# -------------------------------------------
# --------------- Set Display ---------------
# -------------------------------------------

window_height = 600
window_width = 800

game_resolution = (window_width, window_height)
game_window = pygame.display.set_mode(game_resolution) # Windowed
game_surface = pygame.Surface(game_resolution)

zoom_amount = 2
zoomed_resolution = (game_resolution[0] * zoom_amount, game_resolution[1] * zoom_amount)

# ------------------------------------------
# ---------------- Set Rate ----------------
# ------------------------------------------

clock = pygame.time.Clock()
clock_rate = 60

# -----------------------------------------
# -------------- Get Assets ---------------
# -----------------------------------------

import os
print(os.listdir('./assets/campaigns/testCampaign'))

image_tileset = pygame.image.load("./assets/images/tileset.png")
tmx_level = load_pygame("./assets/campaigns/testCampaign/Level1.tmx")

# -----------------------------------------------------
# -------------- Other stuff move later ---------------
# -----------------------------------------------------

camera_pos = [100,100]
# movement_speed = 3



#collision_area = pygame.rect(0, 0, 300, 50)


def handle_input():
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False # Pressing X on window will invoke this. Kinda useless for border though.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: return False # TEMPORARY! REMOVE LATER! Only for testing purposes
    return True

def handle_rendering(player, ui, lighting):
    game_surface.fill((40, 40, 40))
    draw_map(game_surface, tmx_level, camera_pos)
    player.draw(game_surface, camera_pos)

    lighting.draw(game_surface, camera_pos)

    offset_x = (player.rect.centerx - camera_pos[0]) * zoom_amount - game_resolution[0] // 2
    offset_y = (player.rect.centery - camera_pos[1]) * zoom_amount - game_resolution[1] // 2

    scaled_surface = pygame.transform.scale(game_surface, zoomed_resolution)
    game_window.blit(scaled_surface, (-offset_x, -offset_y))

    ui.draw(game_window)

    pygame.display.flip()

def draw_map(surface, tmx_data, camera_pos):
    tw = tmx_data.tilewidth
    th = tmx_data.tileheight
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile_x = (x * tw) - camera_pos[0]
                    tile_y = (y * th) - camera_pos[1]
                    surface.blit(tile, (tile_x, tile_y))

def load_player():
    player_image = pygame.image.load("./assets/sprites/player.png")
    spawn_point = tmx_level.get_object_by_name("spawn_player")
    player_pos = (spawn_point.x, spawn_point.y)
    player_width = 16
    player_height = 24

    return player_image, player_pos, player_width, player_height

def update_camera(camera_pos, player_pos, viewport_width, viewport_height):
    camera_pos[0] = player_pos.x - viewport_width // 2
    camera_pos[1] = player_pos.y - viewport_height // 2


def main():
    print("Starting game!")

    map.create_collision_map(tmx_level)
    player = Player(*load_player())
    ui = UI(player)
    
    lighting = Lighting(window_width, window_height)
    lighting.load_lights_from_map(tmx_level)

    running = True
    while running:
        clock.tick(clock_rate)

        keys = pygame.key.get_pressed()
        player.update(keys)

        update_camera(camera_pos, player.position, game_resolution[0], game_resolution[1])

        running = handle_input()
        handle_rendering(player, ui, lighting)


    print("Exiting game!")
    pygame.quit()

if __name__ == "__main__":
    main()