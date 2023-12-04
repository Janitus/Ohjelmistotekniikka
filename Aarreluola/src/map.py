"""Handles loading all instances, and storing collision / ladder map"""
import pytmx

# pylint: disable=no-member,c-extension-no-member

collision_map = []
ladder_map = []
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
    global collision_map
    global ladder_map

    collision_map.clear()
    ladder_map.clear()

    width, height = tmx_level.width, tmx_level.height

    # Generated
    collision_map = [[False for _ in range(width)] for _ in range(height)]
    ladder_map = [[False for _ in range(width)] for _ in range(height)]
    # End Generated

    for layer in tmx_level.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            set_layer_values(layer, collision_map, ladder_map)

def set_layer_values(layer, collisions, ladders):
    """Sets environment and ladder array values"""
    for y in range(layer.height):
        for x in range(layer.width):
            tile = layer.data[y][x]
            if tile and layer.name == 'Environment':
                collisions[y][x] = True
            if tile and layer.name == 'Ladder':
                ladders[y][x] = True

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
