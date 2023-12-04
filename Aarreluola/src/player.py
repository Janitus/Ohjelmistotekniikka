"""Player resides here."""

import pygame
from character import Character
from projectile_manager import ProjectileManager
# pylint: disable=no-member,c-extension-no-member, too-many-instance-attributes
# Pylint herjaa pygamen jokaisesta ominaisuudesta no-member, joten kytkemme sen pois.
# Disabloimme too-many-instance-attributes, sillä nämä ovat kaikki tarvittavia attribuutteja.

class Player(Character):
    """
    Player is the sole character the user controls.
    Player specific attributes:
    money
    life
    ammo
    max_ammo
    keys (set), stores a number of keys picked in the game and is reset after entering next level
    shot_cooldown (the time between shots until the next shot can be taken)
    projectile_damage
    interactive_mode (used to interact with things on the map, currently only buying items.)
    """
    def __init__(self,image = pygame.image.load("./assets/sprites/player.png"),
                 width=16, height=24):
        super().__init__(image, width, height)
        self.money = 0
        self.life = 3
        self.ammo = 4
        self.max_ammo = 4
        self.keys = set()

        self.invulnerability_duration = 1000
        self.last_shot = -9999
        self.shot_cooldown = 1000
        self.projectile_damage = 1

        self.jump_power = 4
        self.speed = 2
        self.gravity = 0.15
        self.health = 10
        self.max_health = 10

        # The interactive mode is used only for buying currently
        self.interactive_mode = False

    def control (self, keys):
        """Reads the user input and acts upon the instructions"""
        super().update()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_upwards()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_downwards()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move(-self.speed, 0)
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(self.speed, 0)
            self.direction.x = 1
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            self.shoot()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.interactive_mode = True
        else:
            self.interactive_mode = False

    def shoot(self):
        """Shoots a projectile if ammo present"""
        if self.ammo <= 0:
            return False
        if pygame.time.get_ticks() - self.last_shot < self.shot_cooldown:
            return False

        self.last_shot = pygame.time.get_ticks()
        self.ammo -= 1

        self.shoot_projectile()

        return True

    def shoot_projectile(self):
        """Spwans the projectile"""
        projectile = ProjectileManager.create_projectile(
            self.projectile_manager, self.center(), self.direction, "player")
        projectile.speed = 5
        projectile.knock_power = 1.2
        projectile.damage = self.projectile_damage
        projectile.set_size(5, 2)
        projectile.set_color(255, 200, 150)

    def receive_key(self, key_name):
        """Grants the player a key by key_name"""
        self.keys.add(key_name)

    def receive_ammo(self, amount):
        """Grants the player ammo based on amount"""
        if amount <= 0:
            return
        self.ammo += amount
        self.ammo = min(self.ammo, self.max_ammo)

    def receive_life(self, amount):
        """Grants additional lives based on amount"""
        self.life += amount

    def receive_money(self, amount):
        """Grants money which can be used to buy items"""
        self.money += amount

    def purchase_item(self, price):
        """Checks whether enough money for purchase."""
        if price > self.money:
            return False
        self.money -= price
        return True

    def respawn(self):
        """Respawns the player by reducing one life, healing to full and setting dead to false"""
        self.velocity_y = 0
        self.life -= 1
        self.health = self.max_health
        self.dead = False
