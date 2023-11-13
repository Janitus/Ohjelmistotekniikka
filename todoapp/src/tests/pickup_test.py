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

    def test_pickup_grants_multiple(self):
        health_pickup = self.create_pickup({'money': 10, 'life': 1})
        self.player.money = 10
        self.player.life = 1
        health_pickup.apply_to_player(self.player)
        self.assertEqual(self.player.money, 20)
        self.assertEqual(self.player.life, 2)

    def create_pickup(self, attributes):     # Helper function for testing out pickups
        img = pygame.Surface((20, 20))
        pickup = Pickup("testpickup", img, attributes)
        return pickup
