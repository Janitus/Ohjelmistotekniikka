"""Enemy is a child class of Characters."""
import os
import pygame
from map import get_collision_by_coordinate as get_collision
from character import Character

ENEMY_DIRECTORY = "./assets/enemies/"
enemy_templates = {}


class Enemy(Character):
    """
    Enemy is a child class of character
    Enemy specific attributes are:
    melee_damage = The damage player receives when colliding
    melee_knock = The amount of knockup applied to player when hit
    avoid_falls = Behaviour that dictates whether enemy turns directions before falling
    """
    def __init__(self, image, attributes=None):
        if attributes is None:
            attributes = {}
        self.attributes = attributes
        super().__init__(image,
                         attributes.get('width', 16),
                         attributes.get('height', 24))

        self.speed = attributes.get('speed', .5)
        self.melee_damage = attributes.get('melee_damage', 1)
        self.melee_knock = attributes.get('melee_knock', 1.8)
        self.health = attributes.get('health', 1)
        self.max_health = attributes.get('max_health', 1)
        self.gravity = attributes.get('gravity', .15)
        self.avoid_falls = attributes.get('avoid_falls', False)

    def update(self):
        self.patrol()
        super().update()

    def die(self):
        self.dead = True

    def patrol(self):
        """Patrols horizontally until a collision is detected"""
        if self.avoid_falls and self.is_facing_a_fall():
            self.direction.x *= -1

        if not self.collides(self.direction.x * self.speed, 0):
            self.move(self.direction.x * self.speed, 0)
        else:
            self.direction.x *= -1

    def is_facing_a_fall(self):
        """Checks whether there is a ledge ahead, if true, turn around"""
        if self.direction.x > 0 and get_collision(self.position.y+10,
                                                  self.position.x+self.speed) is True:
            return False
        if self.direction.x <= 0 and get_collision(self.position.y+10,
                                                   self.position.x-self.speed) is True:
            return False
        return True


def load_enemy_types():
    """Loads all the enemy types from assets/enemies/ directory"""
    attribute_parsers = {
        'speed': parse_float,
        'melee_damage': parse_int,
        'melee_knock': parse_float,
        'width': parse_int,
        'height': parse_int,
        'health': parse_int,
        'max_health': parse_int,
        'gravity': parse_float,
        'avoid_falls': parse_bool,
    }

    for enemy_name in os.listdir(ENEMY_DIRECTORY):
        enemy_dir = os.path.join(ENEMY_DIRECTORY, enemy_name)
        if os.path.isdir(enemy_dir):
            info_path = os.path.join(enemy_dir, "info.txt")
            image_path = os.path.join(enemy_dir, "image.png")
            if os.path.isfile(info_path) and os.path.isfile(image_path):
                image = pygame.image.load(image_path)
                attributes = {}

                with open(info_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if ':' in line:
                            key, value = line.strip().split(':', 1)
                            parser = attribute_parsers.get(key)
                            if parser:
                                attributes[key] = parser(value)

                enemy_templates[enemy_name] = Enemy(image, attributes)
    return enemy_templates


def parse_bool(value):
    """Helper function to parse booleans from strings."""
    return value.lower() == 'true'

def parse_int(value):
    """Helper function to parse integers from strings."""
    return int(value)

def parse_float(value):
    """Helper function to parse floats from strings."""
    return float(value)



enemy_templates = load_enemy_types()
