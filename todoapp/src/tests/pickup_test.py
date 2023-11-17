import unittest
import player
import game
import pygame
from pickup import Pickup, load_pickup_types


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.pickups = load_pickup_types()
        self.player = player.Player(*game.load_player())

    def test_loading_from_file_gets_templates(self):
        self.assertGreater(len(self.pickups), 0)

    def test_pickup_grants_ammo(self):
        ammo_pickup = self.create_pickup({'ammo': 1})
        self.player.max_ammo = 2
        self.player.ammo = 1
        ammo_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.ammo, 2)

    def test_pickup_grants_health(self):
        health_pickup = self.create_pickup({'health': 1})
        self.player.max_health = 2
        self.player.health = 1
        health_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.health, 2)

    def test_pickup_grants_key(self):
        health_pickup = self.create_pickup({'key': "testkey"})
        health_pickup.apply_to_player(self.player)
        self.assertTrue(self.player.keys.__contains__("testkey"))

    def test_pickup_grants_life(self):
        health_pickup = self.create_pickup({'life': 1})
        self.player.life = 1
        health_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.life, 2)

    def test_pickup_grants_money(self):
        health_pickup = self.create_pickup({'money': 10})
        self.player.money = 10
        health_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.money, 20)

    def test_pickup_grants_max_ammo(self):
        max_ammo_pickup = self.create_pickup({'max_ammo': 10})
        self.player.max_ammo = 10
        max_ammo_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.max_ammo, 20)

    def test_pickup_grants_max_health(self):
        max_health_pickup = self.create_pickup({'max_health': 10})
        self.player.max_health = 10
        max_health_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.max_health, 20)

    def test_pickup_grants_speed(self):
        speed_pickup = self.create_pickup({'speed': 10})
        self.player.speed = 10
        speed_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.speed, 20)

    def test_pickup_sets_damage(self):
        damage_pickup = self.create_pickup({'damage': 20})
        self.player.projectile_damage = 10
        damage_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.projectile_damage, 20)

        # Check that bonus is not additive
        damage_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.projectile_damage, 20)

    def test_pickup_sets_shot_cooldown(self):
        shot_cooldown_pickup = self.create_pickup({'shot_cooldown': 100})
        self.player.shot_cooldown = 1000
        shot_cooldown_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.shot_cooldown, 100)

        # Check that bonus is not additive
        shot_cooldown_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.shot_cooldown, 100)

    def test_pickup_grants_multiple(self):
        health_pickup = self.create_pickup({'money': 10, 'life': 1})
        self.player.money = 10
        self.player.life = 1
        health_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.money, 20)
        self.assertEqual(self.player.life, 2)

    def test_pickup_can_be_bought_with_money (self):
        purchaseable_pickup = self.create_pickup({'price': 10})
        self.player.money = 15
        self.player.purchase_mode = True
        purchaseable_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.money, 5)

    def test_pickup_can_not_be_bought_with_insufficient_money (self):
        purchaseable_pickup = self.create_pickup({'price': 10})
        self.player.money = 5
        self.player.purchase_mode = True
        purchaseable_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.money, 5)

    def test_pickup_is_not_bought_when_purchase_mode_is_false (self):
        purchaseable_pickup = self.create_pickup({'price': 10})
        self.player.money = 15
        self.player.purchase_mode = False
        purchaseable_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.money, 15)

    def create_pickup(self, attributes):     # Helper function for testing out pickups
        img = pygame.Surface((20, 20))
        pickup = Pickup("testpickup", img, attributes)
        return pickup
