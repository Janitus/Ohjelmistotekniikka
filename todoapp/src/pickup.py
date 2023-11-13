import os
import enum
import pygame

PICKUP_DIRECTORY = "./assets/pickups/"
pickup_templates = {}


class PickupType(enum.Enum):
    MONEY = "money"
    HEALTH = "health"
    LIFE = "life"
    AMMO = "ammo"
    KEY = "key"


class Pickup:
    def __init__(self, name, image, attributes):
        self.name = name
        self.image = image
        self.attributes = attributes
        self.rect = self.image.get_rect(center=(0, 0))

    def set_position(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, surface, camera_pos):
        render_pos = (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1])
        surface.blit(self.image, render_pos)

    def apply_to_player(self, player):
        for attr, value in self.attributes.items():
            if attr == PickupType.MONEY.value:
                player.money += value
            elif attr == PickupType.HEALTH.value:
                player.heal(value)
            elif attr == PickupType.LIFE.value:
                player.life += value
            elif attr == PickupType.AMMO.value:
                player.receive_ammo(value)
            elif attr == PickupType.KEY.value:
                player.receive_key(value)


def load_pickup_types():
    for pickup_name in os.listdir(PICKUP_DIRECTORY):
        pickup_dir = os.path.join(PICKUP_DIRECTORY, pickup_name)
        if os.path.isdir(pickup_dir):
            info_path = os.path.join(pickup_dir, "info.txt")
            image_path = os.path.join(pickup_dir, "image.png")
            if os.path.isfile(info_path) and os.path.isfile(image_path):
                # Generated
                with open(info_path, 'r') as f:
                    attributes = {}
                    for line in f:
                        if ':' in line:
                            key, val = line.strip().split(':', 1)
                            if key == PickupType.KEY.value:
                                attributes[key] = val
                            else:
                                attributes[key] = int(val)
                # End gen
                image = pygame.image.load(image_path)
                pickup_templates[pickup_name] = Pickup(
                    pickup_name, image, attributes)
    return pickup_templates


def fetch_pickup_templates(pickup_name):
    return pickup_templates.get(pickup_name)


pickup_templates = load_pickup_types()
