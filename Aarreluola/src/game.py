"""The main game"""
import sys
import os
import pygame
from pytmx.util_pygame import load_pygame
import instance_loader
from player import Player
from enemy import load_enemy_types
from ui.ui import UI
from lighting import Lighting
from renderer import Renderer
from pickup import load_pickup_types
import map
from projectile_manager import ProjectileManager
from gamestate import GameState

# pylint: disable=no-member,c-extension-no-member
# Pylint herjaa pygamen jokaisesta ominaisuudesta no-member, joten kytkemme sen pois

pygame.init()
pygame.display.set_caption("Aarreluola")

# -------------------------------------------
# --------------- Set Display ---------------
# -------------------------------------------

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

game_resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
game_window = pygame.display.set_mode(game_resolution)  # Windowed
game_surface = pygame.Surface(game_resolution)

ZOOM_AMOUNT = 2
zoomed_resolution = (game_resolution[0] * ZOOM_AMOUNT, game_resolution[1] * ZOOM_AMOUNT)

# ------------------------------------------
# ---------------- Set Rate ----------------
# ------------------------------------------

clock = pygame.time.Clock()
CLOCK_RATE = 60

# -----------------------------------------
# -------------- Get Assets ---------------
# -----------------------------------------

image_tileset = pygame.image.load("./assets/images/tileset.png")


def handle_input():
    """Reads input from user"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True

def update_camera(camera_pos, player_pos, viewport_width, viewport_height):
    """Updates camera location based on player position"""
    camera_pos[0] = player_pos.x - viewport_width // 2
    camera_pos[1] = player_pos.y - viewport_height // 2

def handle_zones(game_state):
    """Checks whether player is within a zone."""
    for zone in game_state.zones:
        if zone.can_be_activated(game_state.player):
            messages = zone.activate(game_state)
            if isinstance(messages, str) and "exit" in messages:
                game_state.flag_next_level = True

def handle_pickups(game_state):
    """Checks whether player is colliding with any pickups, and absorbs them if true"""
    for pickup in game_state.pickups:
        if game_state.player.rect.colliderect(pickup.rect):
            if pickup.apply_to_player(game_state.player) is True:
                game_state.pickups.remove(pickup)

def handle_enemies(game_state):
    """Updates enemy logic."""
    for enemy in game_state.enemies:
        if pygame.sprite.collide_rect(game_state.player, enemy):
            if game_state.player.damage(enemy.melee_damage):
                game_state.player.knock_up(enemy.melee_knock)

        enemy.update()
        if enemy.dead:
            game_state.enemies.remove(enemy)

def handle_next_level_flag(game_state):
    """Checks if the flag for next level is set true. If true, move to next level or win game"""
    if game_state.flag_next_level:
        game_state.current_level += 1
        if game_state.current_level > len(game_state.level_order)-1:
            print("YOU WIN")
            game_state.renderer.draw_message_screen("You win!", (20, 100, 20))
            pygame.time.delay(2000)
            handle_quit()
        else:
            game_state.player.keys = set()
            load_level(game_state, "Loading next level")
            print("entering level", game_state.current_level)
        game_state.flag_next_level = False
        return True
    return False

def handle_player_status(game_state):
    """Handles character input, as well as checking for death status"""
    if game_state.player.dead:
        if game_state.player.life > 0:
            load_level(game_state, f"You have died! Lives left {game_state.player.life}")
            pygame.time.delay(1000)
            game_state.player.respawn()
        else:
            game_state.renderer.draw_message_screen("You lose!", (50, 20, 20))
            pygame.time.delay(2000)
            handle_quit()

    keys = pygame.key.get_pressed()
    game_state.player.control(keys)

    if keys[pygame.K_F9]:
        game_state.flag_next_level = True  # Secret cheat button
        pygame.time.delay(100)

    return True

def load_campaign(game_state : GameState):
    """Loads campaign based on input name"""
    campaign_path = "./assets/campaigns/"+game_state.campaign_name+"/order.txt"
    if not os.path.exists(campaign_path):
        handle_quit("Could not find a campaign or 'Order.txt' file to fetch levels from!")

    level_order = []

    try:
        # Generated
        with open(campaign_path, 'r', encoding='utf-8') as file:
            for line in file:
                level_line = line.strip()
                level_order.append(level_line)
        # End generation
        if len(level_order) == 0:
            handle_quit("No levels found within the campaign!")

        return level_order
    except FileNotFoundError as e:
        handle_quit(e)
        return False

def get_level_tmx_file(levelname, game_state):
    """Returns the tiled map file based on name"""
    try:
        return load_pygame("./assets/campaigns/"+game_state.campaign_name+"/"+levelname+".tmx")
    except FileNotFoundError as e:
        handle_quit(e)
        return False


def load_level(game_state, message=""):
    """Loads a new level based on the campaign. Screen message is optional."""

    try:
        game_state.renderer.draw_message_screen(message)
        # --- Map data ---
        game_state.tmx_level = get_level_tmx_file(game_state.level_order[game_state.current_level],
                                                  game_state)
        map.set_layers(game_state.tmx_level)
        map.create_collision_map(game_state.tmx_level)
        game_state.pickups = instance_loader.load_pickups_from_map(game_state.tmx_level)
        actions = instance_loader.load_actions_from_map(game_state.tmx_level)
        game_state.zones = instance_loader.load_zones_from_map(game_state.tmx_level, actions)
        game_state.enemies = instance_loader.load_enemies_from_map(game_state.tmx_level)
        game_state.lighting = Lighting(WINDOW_WIDTH, WINDOW_HEIGHT)
        game_state.lighting.load_lights_from_map(game_state.tmx_level)
        game_state.projectile_manager = ProjectileManager(game_state.player, game_state.enemies)

        # --- Allocations ---
        spawn_point = game_state.tmx_level.get_object_by_name("spawn_player")
        game_state.player.projectile_manager = game_state.projectile_manager
        game_state.player.position = pygame.math.Vector2(spawn_point.x, spawn_point.y)
        for enemy in game_state.enemies:
            enemy.projectile_manager = game_state.projectile_manager
    except ValueError as e:
        handle_quit(e)

def set_up_game_state():
    game_state = GameState()
    game_state.campaign_name = "testCampaign"
    if len(sys.argv) == 2:
        game_state.campaign_name = sys.argv[1]



    game_state.level_order = load_campaign(game_state)
    game_state.player = Player()

    game_state.renderer = Renderer(game_surface, game_window,
                        game_resolution, zoomed_resolution)
    game_state.renderer.zoom_amount = 2
    game_state.renderer.game_state = game_state
    game_state.current_level = 0
    return game_state

def main():
    """Main to run the game on."""
    print("Launching game!")

    load_pickup_types()
    load_enemy_types()

    game_state = set_up_game_state()
    camera_pos = [100, 100]
    ui = UI(game_state.player)

    load_level(game_state, "Entering first level")

    # --- Game loop ---

    running = True
    while running:
        clock.tick(CLOCK_RATE)

        handle_next_level_flag(game_state)
        handle_player_status(game_state)
        handle_enemies(game_state)
        handle_pickups(game_state)
        handle_zones(game_state)
        update_camera(camera_pos, game_state.player.position,
                      game_resolution[0], game_resolution[1])

        game_state.projectile_manager.update()
        running = handle_input()
        game_state.renderer.handle_rendering(ui, camera_pos)

    handle_quit("Exiting game!")


def handle_quit(message = ""):
    """Standard quit. Always used, even if errors present."""
    if message != "":
        print(message)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
