import os
import pygame
import map
from character import Character

ENEMY_DIRECTORY = "./assets/enemies/"
enemy_templates = {}


class Enemy(Character):
    def __init__(self, image, attributes={}):
        self.attributes = attributes
        width = attributes.get('width', 16)
        height = attributes.get('height', 24)
        super().__init__(image, width, height)

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
        if self.avoid_falls and self.is_facing_a_fall():
            self.direction.x *= -1

        if not self.collides(self.direction.x * self.speed, 0):
            self.move(self.direction.x * self.speed, 0)
        else:
            self.direction.x *= -1

    def is_facing_a_fall(self):
        if self.direction.x > 0 and map.get_collision_by_coordinate(self.position.y+10, self.position.x+self.speed) is True:
            return False
        if self.direction.x <= 0 and map.get_collision_by_coordinate(self.position.y+10, self.position.x-self.speed) is True:
            return False
        return True


def load_enemy_types():
    for enemy_name in os.listdir(ENEMY_DIRECTORY):
        enemy_dir = os.path.join(ENEMY_DIRECTORY, enemy_name)
        if os.path.isdir(enemy_dir):
            info_path = os.path.join(enemy_dir, "info.txt")
            image_path = os.path.join(enemy_dir, "image.png")
            if os.path.isfile(info_path) and os.path.isfile(image_path):
                image = pygame.image.load(image_path)
                attributes = {}

                with open(info_path, 'r') as f:
                    for line in f:
                        if ':' in line:
                            key, value = line.strip().split(':', 1)
                            if key == 'speed':
                                attributes['speed'] = float(value)
                            elif key == 'melee_damage':
                                attributes['melee_damage'] = int(value)
                            elif key == 'melee_knock':
                                attributes['melee_knock'] = float(value)
                            elif key == 'width':
                                attributes['width'] = int(value)
                            elif key == 'height':
                                attributes['height'] = int(value)
                            elif key == 'health':
                                attributes['health'] = int(value)
                            elif key == 'max_health':
                                attributes['max_health'] = int(value)
                            elif key == 'gravity':
                                attributes['gravity'] = float(value)
                            elif key == 'avoid_falls':
                                attributes['avoid_falls'] = parse_bool(value)

                # e = Enemy(image,(0,0),attributes)
                enemy_templates[enemy_name] = Enemy(image, attributes)
    return enemy_templates


def fetch_enemy_templates(enemy_name):
    return enemy_templates.get(enemy_name)


def parse_bool(value):  # Helper function to parse booleans from file
    if value.lower() == 'true':
        return True
    return False


enemy_templates = load_enemy_types()
