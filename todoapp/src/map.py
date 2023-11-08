import pytmx, pygame
from pickup import pickups
from pickup import fetch_pickup
from pickup import Pickup
from zone import Zone, PlayerHasKeyCondition
import action

tmx_data = None
collision_map = []
ladder_map = []
pickups_map = []
tile_size = 32

layer_environment = None

def set_layers(tmx_data):
    global layer_environment
    for layer in tmx_data.layers:
        if layer.name == "Environment":
            layer_environment = layer
    if(layer_environment == None): raise ValueError("The layer 'Environment' could not be found in the tmx data!")

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

def load_zones_from_map(tmx_data, actions):
    zones = []
    prefix = "zone"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name.startswith(prefix):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                additional_conditions = []
                zone_actions = []

                key_name = obj.properties.get('key')
                if key_name:
                    additional_conditions.append(PlayerHasKeyCondition(key_name))

                #action_id = obj.properties.get('action')
                #if action_id:
                #    zone_actions.append(actions[action_id])

                for property_name, property_value in obj.properties.items():
                    # The reason we do this like this, is the constraint in tiled that prevents us from having multiple fields with the same name.
                    # Thus, actions must be merely named starting with 'action' + anything after it.

                    if property_name.startswith("action"):
                        action_id = property_value
                        if action_id in actions:
                            zone_actions.append(actions[action_id])

                zones.append(Zone(rect, additional_conditions, zone_actions))
    return zones

def load_actions_from_map(tmx_data):
    actions = {}
    prefix = "action"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name.startswith(prefix):
                print("action",obj)
                if 'destroy' in obj.properties:
                    actions[obj.id] = action.DestroyAction(obj.id, (obj.x, obj.y))

    return actions


# The coordinates sent here are per pixel positions.
def get_collision_by_coordinate(x, y):  return collision_map [int(x) // tile_size][int(y) // tile_size]
def get_ladder_by_coordinate(x, y):     return ladder_map [int(x) // tile_size][int(y) // tile_size]

# ------- Actions -------

def destroy_block(x, y):
    global layer_environment
    pos_x = int(x // tile_size)
    pos_y = int(y // tile_size)
    
    if (0 <= pos_x < len(collision_map[0]) and 0 <= pos_y < len(collision_map)):
        collision_map[pos_y][pos_x] = False
        #layer_environment[pos_x][pos_y] = 0
        if layer_environment and hasattr(layer_environment, 'data'):
            layer_environment.data[pos_y][pos_x] = 0 
