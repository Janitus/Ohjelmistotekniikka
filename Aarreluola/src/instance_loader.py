import pygame
import action
from zone import Zone, PlayerHasKeyCondition
from enemy import enemy_templates, Enemy
from pickup import pickup_templates, Pickup

# pylint: disable=no-member,c-extension-no-member

# --- Enemies ---

def create_enemy_instance(enemy_name, position):
    """Creates a new enemy and returns it based on the template"""

    template = enemy_templates.get(enemy_name)
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
            enemy_instance = create_enemy_instance_if_valid (obj, prefix)
            if enemy_instance:
                loaded_enemies.append(enemy_instance)

    return loaded_enemies

def create_enemy_instance_if_valid (obj, prefix):
    """Creates an enemy instance from the object if it matches the criteria."""
    if obj.name and obj.name.startswith(prefix):
        enemy_type = obj.name[len(prefix):]
        return create_enemy_instance(enemy_type, (obj.x, obj.y))
    return None

# --- Pickups ---

def create_pickup_instance(pickup_name, position):
    """Creates a pickup instance based on the templates"""
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

                loaded_pickups.append(pickup_instance)
    return loaded_pickups

# --- Zones ---

def load_zones_from_map(tmx_data, actions):
    """Loads all the zones from a map file and returns an array of instanced zones"""
    zones = []
    prefix = "zone"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name and obj.name.startswith(prefix):
                create_zone_and_actions(obj,actions,zones)
    return zones

def create_zone_and_actions (obj, actions, zones):
    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    additional_conditions = []
    zone_actions = []

    for property_name, property_value in obj.properties.items():
        if property_name.startswith("action"):
            action_id = property_value
            if action_id in actions:
                zone_actions.append(actions[action_id])

        if property_name.startswith("exit"):
            exit_action = action.ExitAction()
            zone_actions.append(exit_action)

        if property_name.startswith("key"):
            key_name = obj.properties.get('key')
            key_condition = PlayerHasKeyCondition(key_name)
            additional_conditions.append(key_condition)

    zones.append(Zone(rect, additional_conditions, zone_actions))

# --- Actions ---

def load_actions_from_map(tmx_data):
    """Loads all the actions from a map file."""
    actions = {}
    prefix = "action"
    for object_group in tmx_data.objectgroups:
        for obj in object_group:
            if obj.name and obj.name.startswith(prefix):
                create_action_by_type(actions,obj)

    return actions

def create_action_by_type(actions, obj):
    if 'destroy' in obj.properties:
        actions[obj.id] = action.DestroyAction(
            obj.id, (obj.x, obj.y))
    if 'damage' in obj.properties:
        damage_value = damage_value = obj.properties.get('damage', 0)
        knockup_value = damage_value = obj.properties.get('damage_knock', 0)
        actions[obj.id] = action.DamageAction(
            obj.id, damage_value, knockup_value)
    if 'knockup' in obj.properties:
        knockup_value = obj.properties['knockup']
        actions[obj.id] = action.KnockupAction(
            obj.id, knockup_value)
