import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from enemy import Enemy
from ui import UI
from lighting import Lighting
from renderer import Renderer
from pickup import load_pickups
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


def handle_input():
    #keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False # Pressing X on window will invoke this. Kinda useless for border though.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: return False # TEMPORARY! REMOVE LATER! Only for testing purposes
    return True

def load_player():
    player_image = pygame.image.load("./assets/sprites/player.png")
    spawn_point = tmx_level.get_object_by_name("spawn_player")
    player_pos = (spawn_point.x, spawn_point.y)
    player_width = 16
    player_height = 24

    return player_image, player_pos, player_width, player_height

def load_enemies():
    enemy_image = pygame.image.load("./assets/sprites/enemy0.png")
    enemy_width = 16
    enemy_height = 24
    enemies = []

    for object_group in tmx_level.objectgroups:
        for obj in object_group:
            if obj.name == "spawn_enemy0":
                enemy_pos = (obj.x, obj.y)
                enemy = Enemy(enemy_image, enemy_pos, enemy_width, enemy_height)
                enemies.append(enemy)

    return enemies

def update_camera(camera_pos, player_pos, viewport_width, viewport_height):
    camera_pos[0] = player_pos.x - viewport_width // 2
    camera_pos[1] = player_pos.y - viewport_height // 2

def main():
    print("Starting game!")

    load_pickups()

    pickups = None
    actions = None
    zones = None

    try:
        map.set_layers(tmx_level)
        map.create_collision_map(tmx_level)
        pickups = map.load_pickups_from_map(tmx_level)
        actions = map.load_actions_from_map(tmx_level)
        zones = map.load_zones_from_map(tmx_level, actions)
    except ValueError as e:
        print(e)
        pygame.quit()

    renderer = Renderer(game_surface, tmx_level, game_window, game_resolution, zoomed_resolution)
    renderer.set_zoom_amount(2)

    player = Player(*load_player())
    ui = UI(player)

    enemies = load_enemies()
    
    lighting = Lighting(window_width, window_height)
    lighting.load_lights_from_map(tmx_level)

    running = True
    while running:
        clock.tick(clock_rate)

        keys = pygame.key.get_pressed()
        player.update(keys)

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                if (player.damage(enemy.melee_damage)):
                    player.knock_up(enemy.melee_knock)

            enemy.update()

        for pickup in pickups:
            if player.rect.colliderect(pickup.rect):
                pickup.apply_to_player(player)
                pickups.remove(pickup)

        for zone in zones:
            if zone.is_activated(player):
                zone.activate()
                continue
            else:
                continue

        update_camera(camera_pos, player.position, game_resolution[0], game_resolution[1])

        running = handle_input()
        renderer.handle_rendering(player, ui, lighting, camera_pos, pickups, enemies)


    print("Exiting game!")
    pygame.quit()

if __name__ == "__main__":
    main()