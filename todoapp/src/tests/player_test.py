import unittest
import player, game
import pygame

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = player.Player(*game.load_player())
        self.player.health = 10
        self.player.max_health = 10
        self.player.max_ammo = 4
        self.player.ammo = 1
        self.player.width = 16
        self.player.height = 24
        self.player.money = 50
        self.player.life = 3
        self.player.speed = 3

    # Health

    def test_max_hp(self):
        self.assertEqual(self.player.max_health, 10)

    def test_current_hp(self):
        self.assertEqual(self.player.health, 10)

    def test_damage_reduces_hp(self):
        self.player.damage(5)
        self.assertEqual(self.player.health, 5)

    def test_block_damage_within_invulnerability_time(self):
        self.player.damage(2)
        self.assertEqual(self.player.health, 8)
        self.player.damage(2)
        self.assertEqual(self.player.health, 8)

    def test_block_damage_outside_invulnerability_time(self):
        self.player.invulnerability_duration = 50
        self.player.damage(2)
        self.assertEqual(self.player.health, 8)
        pygame.time.delay(100)
        self.player.damage(2)
        self.assertEqual(self.player.health, 6)

    def test_heal_increases_hp(self):
        self.player.health = 5
        self.player.heal(3)
        self.assertEqual(self.player.health, 8)
        self.player.heal(3)
        self.assertEqual(self.player.health, 10)

    def test_current_health_does_not_follow_max_hp(self):
        self.player.max_health = 15
        self.assertEqual(self.player.max_health, 15)
        self.assertEqual(self.player.health, 10)

    # Shooting & Ammo

    def test_ammo_amount(self):
        self.assertEqual(self.player.ammo, 1)

    def test_max_ammo_amount(self):
        self.assertEqual(self.player.max_ammo, 4)

    def test_gain_ammo(self):
        self.player.receive_ammo(1)
        self.assertEqual(self.player.ammo, 2)
        self.player.receive_ammo(10)
        self.assertEqual(self.player.ammo, 4)

    def test_shooting_with_ammo(self):
        self.assertTrue(self.player.shoot())
        self.assertEqual(self.player.ammo, 0)

    def test_shooting_without(self):
        self.player.ammo = 0
        self.assertFalse(self.player.shoot())
        self.assertEqual(self.player.ammo, 0)

    def test_shooting_too_fast(self):
        self.player.shot_cooldown = 100
        self.player.ammo = 2
        self.assertTrue(self.player.shoot())
        pygame.time.delay(50)
        self.assertFalse(self.player.shoot())
        

    def test_shooting_on_time(self):
        self.player.shot_cooldown = 100
        self.player.ammo = 2
        self.assertTrue(self.player.shoot())
        pygame.time.delay(150)
        self.assertTrue(self.player.shoot())

    # Size

    def test_width(self):
        self.assertEqual(self.player.width, 16)

    def test_height(self):
        self.assertEqual(self.player.height, 24)
    
    # Life

    def test_lives(self):
        self.assertEqual(self.player.life, 3)

    def test_gain_lives(self):
        self.player.receive_life(1)
        self.assertEqual(self.player.life, 4)

    # Money

    def test_money(self):
        self.assertEqual(self.player.money, 50)

    def test_gain_money(self):
        self.player.receive_money(20)
        self.assertEqual(self.player.money, 70)

    def test_purchase_with_enough_money(self):
        self.assertTrue(self.player.purchase_item(20))
        self.assertEqual(self.player.money, 30)

    def test_purchase_with_not_enough_money(self):
        self.assertFalse(self.player.purchase_item(60))
        self.assertEqual(self.player.money, 50)

    # Keys

    def test_player_has_no_key(self):
        self.assertEqual(len(self.player.keys), 0)

    def test_player_receives_some_key(self):
        self.player.receive_key ("somekey")
        self.assertEqual(len(self.player.keys), 1)
        self.assertTrue(self.player.keys.__contains__("somekey"))

    # Other stats

    def test_speed(self):
        self.assertEqual(self.player.speed, 3)