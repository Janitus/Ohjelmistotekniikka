import pytmx

tmx_data = None
collision_map = []
ladder_map = []

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



# The coordinates sent here are raw and in an int format.
def get_collision_by_coordinate(x, y):  return collision_map [int(x) // tile_size][int(y) // tile_size]
def get_ladder_by_coordinate(x, y):     return ladder_map [int(x) // tile_size][int(y) // tile_size]
