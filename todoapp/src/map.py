import pytmx, pygame
from pickup import pickups
from pickup import fetch_pickup
from pickup import Pickup
from zone import Zone, PlayerHasKeyCondition

tmx_data = None
collision_map = []
ladder_map = []
pickups_map = []
tile_size = 32

def create_collision_map(tmx_level):
    global tmx_data
    tmx_data = tmx_level
    global collision_map
    global ladder_map

    collision_map.clear()
    ladder_map.clear()

    width, height = tmx_data.width, tmx_data.height

    # Generated
    collision_map = [[False for _ in range(width)] for _ in range(height)]
    ladder_map =    [[False for _ in range(width)] for _ in range(height)]
    # End Generated

    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for y in range(layer.height):
                for x in range(layer.width):
                    tile = layer.data[y][x]
                    if tile:
                        if layer.name == 'Environment': collision_map[y][x] = True
                        if layer.name == 'Ladder': ladder_map[y][x] = True
    print("map data created!")


def create_pickup_instance(pickup_name, position):
    template = pickups.get(pickup_name)
    if template:
        new_pickup = Pickup(template.name, template.image, template.attributes.copy())
        new_pickup.set_position(position)
        return new_pickup
    return None


def load_pickups_from_map(tmx_data):
    loaded_pickups = []
    prefix = "pickup_"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name.startswith(prefix):
                pickup_type = obj.name[len(prefix):]  # We remove the prefix to get the actual pickup name
                pickup_instance = create_pickup_instance(pickup_type, (obj.x, obj.y))
                if pickup_instance:
                    loaded_pickups.append(pickup_instance)
    return loaded_pickups

def load_zones_from_map(tmx_data):
    zones = []
    prefix = "zone"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name.startswith(prefix):
                print("zone",obj)
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                additional_conditions = []
                key_name = obj.properties.get('key')
                if key_name:
                    additional_conditions.append(PlayerHasKeyCondition(key_name))
                zones.append(Zone(rect, additional_conditions))
    return zones


# The coordinates sent here are per pixel positions.
def get_collision_by_coordinate(x, y):  return collision_map [int(x) // tile_size][int(y) // tile_size]
def get_ladder_by_coordinate(x, y):     return ladder_map [int(x) // tile_size][int(y) // tile_size]
