"""Pickups are items a player can pick up to empower themselves"""
import os
import enum
import pygame

# pylint: disable=no-member,c-extension-no-member
pygame.init()
pygame.font.init()

PICKUP_DIRECTORY = "./assets/pickups/"
pickup_templates = {}
font = pygame.font.Font(None, 14)


class PickupType(enum.Enum):
    """Enum to handle pickup types"""
    MONEY = "money"
    HEALTH = "health"
    MAX_HEALTH = "max_health"
    LIFE = "life"
    AMMO = "ammo"
    MAX_AMMO = "max_ammo"
    DAMAGE = "damage"
    SHOT_COOLDOWN = "shot_cooldown"
    SPEED = "speed"
    KEY = "key"
    PRICE = "price"



class Pickup:
    """An item that can be picked up for benefits."""
    def __init__(self, name, image, attributes):
        self.name = name
        self.image = image
        self.attributes = attributes
        self.price = self.attributes.get("price", 0)

        self.rect = self.image.get_rect(center=(0, 0))

    def set_position(self, position):
        """Sets the position of the pickup."""
        self.rect = self.image.get_rect(center=position)

    def draw(self, surface, camera_pos):
        """Draws the pickup on the surface based on camera position"""
        render_pos = (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1])
        surface.blit(self.image, render_pos)

        if self.price > 0:
            price_text = font.render(str(self.price)+"€", True, (255, 255, 255))
            text_rect = price_text.get_rect(center=(self.rect.centerx - camera_pos[0],
                                                    self.rect.centery - camera_pos[1] - 12))
            surface.blit(price_text, text_rect)

    def apply_to_player(self, player):
        """Applies the bonuses available in attribute list to the player, excluding "price"."""

        if self.price > 0:
            if player.interactive_mode is False:
                return False
            if player.purchase_item(self.price) is False:
                return False

        attribute_actions = {
            PickupType.MONEY.value: lambda p, v: setattr(p, 'money', p.money + v),
            PickupType.HEALTH.value: lambda p, v: p.heal(v),
            PickupType.MAX_HEALTH.value: lambda p, v: setattr(p, 'max_health', p.max_health + v),
            PickupType.LIFE.value: lambda p, v: setattr(p, 'life', p.life + v),
            PickupType.AMMO.value: lambda p, v: p.receive_ammo(v),
            PickupType.MAX_AMMO.value: lambda p, v: setattr(p, 'max_ammo', p.max_ammo + v),
            PickupType.SPEED.value: lambda p, v: setattr(p, 'speed', p.speed + v),
            PickupType.DAMAGE.value: lambda p, v: setattr(p, 'projectile_damage', v),
            PickupType.SHOT_COOLDOWN.value: lambda p, v: setattr(p, 'shot_cooldown', v),
            PickupType.KEY.value: lambda p, v: p.receive_key(v),
        }

        for attr, value in self.attributes.items():
            action = attribute_actions.get(attr)
            if action:
                action(player, value)

        return True


def load_pickup_types():
    """Loads all the pickup templates from assets/pickups/ for instantiation"""
    for pickup_name in os.listdir(PICKUP_DIRECTORY):
        pickup_dir = os.path.join(PICKUP_DIRECTORY, pickup_name)
        if os.path.isdir(pickup_dir):
            info_path = os.path.join(pickup_dir, "info.txt")
            image_path = os.path.join(pickup_dir, "image.png")
            if os.path.isfile(info_path) and os.path.isfile(image_path):
                # Generated
                with open(info_path, 'r', encoding='utf-8') as f:
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



pickup_templates = load_pickup_types()
