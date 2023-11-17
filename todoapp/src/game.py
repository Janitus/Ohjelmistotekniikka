"""The main game"""
import sys
import os
import pygame
from pytmx.util_pygame import load_pygame
from player import Player
from enemy import load_enemy_types
from ui import UI
from lighting import Lighting
from renderer import Renderer
from pickup import load_pickup_types
import map
from projectile_manager import ProjectileManager

pygame.init()
pygame.display.set_caption("Placeholder Name")

# -------------------------------------------
# --------------- Set Display ---------------
# -------------------------------------------

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

game_resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
game_window = pygame.display.set_mode(game_resolution)  # Windowed
game_surface = pygame.Surface(game_resolution)

ZOOM_AMOUNT = 2
zoomed_resolution = (
    game_resolution[0] * ZOOM_AMOUNT, game_resolution[1] * ZOOM_AMOUNT)

# ------------------------------------------
# ---------------- Set Rate ----------------
# ------------------------------------------

clock = pygame.time.Clock()
CLOCK_RATE = 60

# -----------------------------------------
# -------------- Get Assets ---------------
# -----------------------------------------

image_tileset = pygame.image.load("./assets/images/tileset.png")

# -------------------------------------------
# -------------- Other stuff  ---------------
# -------------------------------------------


TMX_LEVEL = None
PICKUPS = None
ZONES = None
ENEMIES = None
PROJECTILE_MANAGER = None
LIGHTING = None
CURRENT_LEVEL = None
RENDERER = None
LEVEL_ORDER = None
FLAG_NEXT_LEVEL = None
CAMPAIGN_NAME = None


def handle_input():
    """Reads input from user"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def load_player():
    """Loads the player with predefined values"""
    player_image = pygame.image.load("./assets/sprites/player.png")
    player_width = 16
    player_height = 24

    return player_image, player_width, player_height


def update_camera(camera_pos, player_pos, viewport_width, viewport_height):
    """Updates camera location based on player position"""
    camera_pos[0] = player_pos.x - viewport_width // 2
    camera_pos[1] = player_pos.y - viewport_height // 2


def handle_zones(zones, player):
    """Checks whether player is within a zone."""
    global FLAG_NEXT_LEVEL
    for zone in zones:
        if zone.is_activated(player):
            messages = zone.activate()
            if isinstance(messages, str) and "exit" in messages:
                FLAG_NEXT_LEVEL = True


def handle_pickups(pickups, player):
    """Checks whether player is colliding with any pickups, and absorbs them if true"""
    for pickup in pickups:
        if player.rect.colliderect(pickup.rect):
            if pickup.apply_to_player(player) is True:
                pickups.remove(pickup)


def handle_enemies(enemies, player):
    """Updates enemy logic, also checks for collisions between player and enemy to perform attacks. Checks for death."""
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            if player.damage(enemy.melee_damage):
                player.knock_up(enemy.melee_knock)

        enemy.update()
        if enemy.dead:
            enemies.remove(enemy)


def load_campaign():
    """Loads campaign based on input name"""
    global CAMPAIGN_NAME
    campaign_path = "./assets/campaigns/"+CAMPAIGN_NAME+"/order.txt"
    if not os.path.exists(campaign_path):
        quit("Could not find a campaign or 'Order.txt' file to fetch levels from!")

    level_order = []

    try:
        # Generated
        with open(campaign_path, 'r') as file:
            for line in file:
                level_line = line.strip()
                level_order.append(level_line)
        # End generation
        if len(level_order) == 0:
            quit("No levels found within the campaign!")

        return level_order
    except FileNotFoundError as e:
        quit(e)



def get_level_tmx_file(levelname):
    """Returns the tiled map file based on name"""
    try:
        return load_pygame("./assets/campaigns/"+CAMPAIGN_NAME+"/"+levelname+".tmx")
    except FileNotFoundError as e:
        quit(e)


def load_level(player, message=""):
    """Loads a new level based on the campaign. Message is optional, and is displayed on the loading screen."""
    global TMX_LEVEL
    global PICKUPS
    global ZONES
    global ENEMIES
    global PROJECTILE_MANAGER
    global LIGHTING

    try:
        RENDERER.draw_message_screen(message)
        # --- Map data ---
        TMX_LEVEL = get_level_tmx_file(LEVEL_ORDER[CURRENT_LEVEL])
        map.set_layers(TMX_LEVEL)
        map.create_collision_map(TMX_LEVEL)
        PICKUPS = map.load_pickups_from_map(TMX_LEVEL)
        actions = map.load_actions_from_map(TMX_LEVEL)
        ZONES = map.load_zones_from_map(TMX_LEVEL, actions)
        ENEMIES = map.load_enemies_from_map(TMX_LEVEL)
        LIGHTING = Lighting(WINDOW_WIDTH, WINDOW_HEIGHT)
        LIGHTING.load_lights_from_map(TMX_LEVEL)

        # --- Managers ---
        PROJECTILE_MANAGER = ProjectileManager(player, ENEMIES)

        # --- Allocations ---
        spawn_point = TMX_LEVEL.get_object_by_name("spawn_player")
        player.projectile_manager = PROJECTILE_MANAGER
        player.position = pygame.math.Vector2(spawn_point.x, spawn_point.y)
        for enemy in ENEMIES:
            enemy.projectile_manager = PROJECTILE_MANAGER
        RENDERER.tmx_level = TMX_LEVEL
    except ValueError as e:
        quit(e)


def main():
    """Main function to run the game on."""
    print("Launching game!")

    global CAMPAIGN_NAME
    CAMPAIGN_NAME = "testCampaign"
    if len(sys.argv) == 2:
        CAMPAIGN_NAME = sys.argv[1]

    # --- Load templates ---

    load_pickup_types()
    load_enemy_types()

    # --- Load permanent ---

    camera_pos = [100, 100]
    global RENDERER
    global LEVEL_ORDER

    LEVEL_ORDER = load_campaign()
    player = Player(*load_player())
    ui = UI(player)
    RENDERER = Renderer(game_surface, game_window,
                        game_resolution, zoomed_resolution)
    RENDERER.zoom_amount = 2

    # --- Load temporal ---

    global TMX_LEVEL
    global FLAG_NEXT_LEVEL  # Used to flag when next level should be loaded
    global PICKUPS
    global ZONES
    global ENEMIES
    global PROJECTILE_MANAGER
    global LIGHTING
    global CURRENT_LEVEL

    TMX_LEVEL = None
    FLAG_NEXT_LEVEL = False
    PICKUPS = None
    ZONES = None
    ENEMIES = None
    PROJECTILE_MANAGER = None
    LIGHTING = None
    CURRENT_LEVEL = 0

    load_level(player, "Entering first level")

    # --- Game loop ---

    running = True
    while running:
        clock.tick(CLOCK_RATE)
        if FLAG_NEXT_LEVEL:
            CURRENT_LEVEL += 1
            if CURRENT_LEVEL > len(LEVEL_ORDER)-1:
                print("YOU WIN")
                RENDERER.draw_message_screen("You win!", (20, 100, 20))
                pygame.time.delay(2000)

                break
            else:
                load_level(player, "Loading next level")
                print("entering level", CURRENT_LEVEL)
            FLAG_NEXT_LEVEL = False

        if player.dead:
            if player.life > 0:
                load_level(player, f"You have died! Lives left {player.life}")
                pygame.time.delay(1000)
                player.respawn()
            else:
                RENDERER.draw_message_screen("You lose!", (50, 20, 20))
                pygame.time.delay(2000)
                break

        keys = pygame.key.get_pressed()
        player.update(keys)

        if keys[pygame.K_F9]:
            FLAG_NEXT_LEVEL = True  # Secret cheat button
            pygame.time.delay(100)

        handle_enemies(ENEMIES, player)
        handle_pickups(PICKUPS, player)
        handle_zones(ZONES, player)
        update_camera(camera_pos, player.position,
                      game_resolution[0], game_resolution[1])

        PROJECTILE_MANAGER.update()

        running = handle_input()
        RENDERER.handle_rendering(
            player, ui, LIGHTING, camera_pos, PICKUPS, ENEMIES, PROJECTILE_MANAGER)

    quit("Exiting game!")


def quit(message):
    """Standard quit. Always used, even if errors present."""
    if message != "":
        print(message)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
