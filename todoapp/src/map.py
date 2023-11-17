"""Handles loading all instances of pickups, enemies, zones and actions. Also used to read for collisions and climbable locations. Can be altered runtime via destroy_blocks()"""
import pytmx
import pygame
from zone import Zone, PlayerHasKeyCondition
import action

TMX_DATA = None
collision_map = []
ladder_map = []
pickups_map = []
TILE_SIZE = 32

LAYER_ENVIRONMENT = None


def set_layers(tmx_data):
    """Precomputes layers for later use. Right now, it's just the 'Environment' layer"""
    global LAYER_ENVIRONMENT
    for layer in tmx_data.layers:
        if layer.name == "Environment":
            LAYER_ENVIRONMENT = layer
    if LAYER_ENVIRONMENT is None:
        raise ValueError(
            "The layer 'Environment' could not be found in the tmx data!")


def create_collision_map(tmx_level):
    """Creates a collision map that anything that can collide will read from"""
    global TMX_DATA
    TMX_DATA = tmx_level
    global collision_map
    global ladder_map

    collision_map.clear()
    ladder_map.clear()

    width, height = TMX_DATA.width, TMX_DATA.height

    # Generated
    collision_map = [[False for _ in range(width)] for _ in range(height)]
    ladder_map = [[False for _ in range(width)] for _ in range(height)]
    # End Generated

    for layer in TMX_DATA.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for y in range(layer.height):
                for x in range(layer.width):
                    tile = layer.data[y][x]
                    if tile:
                        if layer.name == 'Environment':
                            collision_map[y][x] = True
                        if layer.name == 'Ladder':
                            ladder_map[y][x] = True

# --- Pickups ---


def create_pickup_instance(pickup_name, position):
    """Creates a pickup instance based on the templates"""
    from pickup import pickup_templates
    from pickup import Pickup
    template = pickup_templates.get(pickup_name)
    if template:
        new_pickup = Pickup(template.name, template.image,
                            template.attributes.copy())
        new_pickup.set_position(position)
        return new_pickup
    return None


def load_pickups_from_map(tmx_data):
    """Loads all the pickups from a map file and returns an array of instanced pickups"""
    loaded_pickups = []
    prefix = "pickup_"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name and obj.name.startswith(prefix):
                pickup_type = obj.name[len(prefix):]
                pickup_instance = create_pickup_instance(
                    pickup_type, (obj.x, obj.y))
                if pickup_instance:
                    loaded_pickups.append(pickup_instance)
    return loaded_pickups

# --- Enemies ---


def create_enemy_instance(enemy_name, position):
    """Creates a new enemy and returns it based on the template"""
    from enemy import enemy_templates
    from enemy import Enemy

    template = enemy_templates.get(enemy_name)
    # print("ASAD",template)
    if template:
        new_enemy = Enemy(template.image, template.attributes)
        new_enemy.position = pygame.math.Vector2(*position)
        return new_enemy
    return None


def load_enemies_from_map(tmx_data):
    """Loads all the enemies from a map file and returns an array of instanced enemies"""
    loaded_enemies = []
    prefix = "spawn_"

    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name and obj.name.startswith(prefix):
                enemy_type = obj.name[len(prefix):]
                enemy_instance = create_enemy_instance(
                    enemy_type, (obj.x, obj.y))
                # print("ASAD",enemy_type, enemy_instance)
                if enemy_instance:
                    loaded_enemies.append(enemy_instance)

    return loaded_enemies

# --- Zones ---


def load_zones_from_map(tmx_data, actions):
    """Loads all the zones from a map file and returns an array of instanced zones"""
    zones = []
    prefix = "zone"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name and obj.name.startswith(prefix):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                additional_conditions = []
                zone_actions = []

                key_name = obj.properties.get('key')
                if key_name:
                    additional_conditions.append(
                        PlayerHasKeyCondition(key_name))

                for property_name, property_value in obj.properties.items():
                    # The reason we do this like this, is the constraint in tiled that prevents us from having multiple fields with the same name.
                    # Thus, actions must be merely named starting with 'action' + anything after it.

                    if property_name.startswith("action"):
                        action_id = property_value
                        if action_id in actions:
                            zone_actions.append(actions[action_id])

                    if property_name.startswith("exit"):
                        exit_action = action.ExitAction()
                        zone_actions.append(exit_action)

                zones.append(Zone(rect, additional_conditions, zone_actions))
    return zones

# --- Actions ---


def load_actions_from_map(tmx_data):
    """Loads all the actions from a map file and returns an array of instanced actions. Assigns IDs to them for later identification, based on the ID system in tiled."""
    actions = {}
    prefix = "action"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name and obj.name.startswith(prefix):
                if 'destroy' in obj.properties:
                    actions[obj.id] = action.DestroyAction(
                        obj.id, (obj.x, obj.y))

    return actions


# The coordinates sent here are per pixel positions.
def get_collision_by_coordinate(x, y):
    """Returns true/false based on the tile coordinate. If true, collision is present."""
    return collision_map[int(x) // TILE_SIZE][int(y) // TILE_SIZE]


def get_ladder_by_coordinate(x, y):
    """Returns true/false based on the ladder coordinate. If true, tile is climbable."""
    return ladder_map[int(x) // TILE_SIZE][int(y) // TILE_SIZE]

# ------- Runtime map functions -------


def destroy_block(x, y):
    """Destroys a block in the environment based on the location."""
    pos_x = int(x // TILE_SIZE)
    pos_y = int(y // TILE_SIZE)

    if (0 <= pos_x < len(collision_map[0]) and 0 <= pos_y < len(collision_map)):
        collision_map[pos_y][pos_x] = False
        if LAYER_ENVIRONMENT and hasattr(LAYER_ENVIRONMENT, 'data'):
            LAYER_ENVIRONMENT.data[pos_y][pos_x] = 0
