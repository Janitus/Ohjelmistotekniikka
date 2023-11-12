import pygame
from pytmx.util_pygame import load_pygame
from player import Player
from enemy import Enemy
from ui import UI
from lighting import Lighting
from renderer import Renderer
from pickup import load_pickup_types
import map
from projectile_manager import ProjectileManager

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
#print(os.listdir('./assets/campaigns/testCampaign'))

image_tileset = pygame.image.load("./assets/images/tileset.png")
tmx_level = None

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
    player_width = 16
    player_height = 24

    return player_image, player_width, player_height

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

def handle_zones(zones, player):
    global flag_next_level
    for zone in zones:
        if zone.is_activated(player):
            messages = zone.activate()
            if isinstance(messages, str) and "exit" in messages:
                flag_next_level = True

def handle_pickups(pickups, player):
    for pickup in pickups:
        if player.rect.colliderect(pickup.rect):
            pickup.apply_to_player(player)
            pickups.remove(pickup)

def handle_enemies(enemies, player):
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                if (player.damage(enemy.melee_damage)):
                    player.knock_up(enemy.melee_knock)

            enemy.update()
            if (enemy.dead):
                enemies.remove(enemy)

def load_campaign(campaign_name):
    campaign_path = "./assets/campaigns/"+campaign_name+"/order.txt"
    level_order = []

    try:
        # Generated
        with open(campaign_path, 'r') as file:
            for line in file:
                level_line = line.strip()
                level_order.append(level_line)
        # End generation
        if (level_order == 0): quit("No levels found within the campaign!")

        return level_order
    except FileNotFoundError as e:
        quit(e)

def get_level_tmx_file(levelname):
    try:
        return load_pygame("./assets/campaigns/testCampaign/"+levelname+".tmx")
    except FileNotFoundError as e:
        quit(e)

def load_level(player, message=""):
    global tmx_level
    global pickups
    global zones
    global enemies
    global projectile_manager
    global lighting
    global current_level
    global renderer

    try:
        renderer.draw_message_screen(message)
        tmx_level = get_level_tmx_file(level_order[current_level])
        map.set_layers(tmx_level)
        map.create_collision_map(tmx_level)
        pickups = map.load_pickups_from_map(tmx_level)
        actions = map.load_actions_from_map(tmx_level)
        zones = map.load_zones_from_map(tmx_level, actions)
        enemies = load_enemies()
        projectile_manager = ProjectileManager(player, enemies)
        spawn_point = tmx_level.get_object_by_name("spawn_player")
        player.projectile_manager = projectile_manager
        player.position = pygame.math.Vector2(spawn_point.x, spawn_point.y)
        lighting = Lighting(window_width, window_height)
        lighting.load_lights_from_map(tmx_level)
        for enemy in enemies:enemy.projectile_manager = projectile_manager
        renderer.tmx_level = tmx_level
    except ValueError as e:
        quit(e)

def main():
    print("Launching game!")

    # --- Load templates ---

    load_pickup_types()
    #load_enemy_types() todo

    # --- Load permanent ---

    global renderer
    global level_order

    player = Player(*load_player())
    ui = UI(player)
    renderer = Renderer(game_surface, game_window, game_resolution, zoomed_resolution)
    renderer.zoom_amount = 2
    campaign_name = "testCampaign"
    level_order = load_campaign(campaign_name)

    # --- Load temporal ---

    global tmx_level
    global flag_next_level # Used to flag when next level should be loaded
    global pickups
    global zones
    global enemies
    global projectile_manager
    global lighting
    global current_level

    tmx_level = None
    flag_next_level = False
    pickups = None
    zones = None
    enemies = None
    projectile_manager = None
    lighting = None
    current_level = 0

    load_level(player, "Entering first level")
    
    # --- Game loop ---

    running = True
    while running:
        clock.tick(clock_rate)
        if(flag_next_level):
            current_level += 1
            if(current_level > len(level_order)-1):
                print("YOU WIN")
                renderer.draw_message_screen("You win!",(20,100,20))
                pygame.time.delay(1000)

                break
            else:
                load_level(player, "Loading next level")
                print("entering level",current_level)
            flag_next_level = False

        if(player.dead):
            if(player.life > 0):
                load_level(player, f"You have died! Lives left {player.life}")
                pygame.time.delay(1000)
                player.respawn()
            else:
                renderer.draw_message_screen("You lose!", (50,20,20))
                pygame.time.delay(1000)
                break

        keys = pygame.key.get_pressed()
        player.update(keys)

        if keys[pygame.K_F9]:
            flag_next_level = True # Secret cheat button
            pygame.time.delay(100)

        handle_enemies(enemies, player)
        handle_pickups(pickups, player)
        handle_zones(zones, player)
        update_camera(camera_pos, player.position, game_resolution[0], game_resolution[1])

        projectile_manager.update()

        running = handle_input()
        renderer.handle_rendering(player, ui, lighting, camera_pos, pickups, enemies, projectile_manager)


    quit("Exiting game!")

def quit(message):
    if message != "": print(message)
    pygame.quit()

if __name__ == "__main__":
    main()