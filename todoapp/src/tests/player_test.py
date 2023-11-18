import unittest
import pygame
import player
import character
from unittest.mock import patch
from projectile_manager import ProjectileManager

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = player.Player()
        self.player.health = 10
        self.player.max_health = 10
        self.player.max_ammo = 4
        self.player.ammo = 1
        self.player.width = 16
        self.player.height = 24
        self.player.money = 50
        self.player.life = 3
        self.player.speed = 3
        self.key = self.get_all_false_keys()

    # Health

    def test_max_hp(self):
        self.assertEqual(self.player.max_health, 10)

    def test_current_hp(self):
        self.assertEqual(self.player.health, 10)

    def test_damage_reduces_hp(self):
        self.player.damage(5)
        self.assertEqual(self.player.health, 5)

    def test_fatal_damage_kills(self):
        self.player.damage(99)
        self.assertEqual(self.player.health, 0)
        self.assertTrue(self.player.dead)

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

    # Respawn

    def test_respawn_reduces_life_by_one(self):
        self.player.respawn()
        self.assertEqual(self.player.life, 2)

    def test_respawn_heals_player_to_full(self):
        self.player.max_health = 10
        self.player.health = 5
        self.player.respawn()
        self.assertEqual(self.player.health, 10)

    def test_respawn_sets_dead_to_false(self):
        self.player.dead = True
        self.player.respawn()
        self.assertFalse(self.player.dead)

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

    # Shooting

    @patch('player.Player.shoot_projectile')
    def test_shooting_with_ammo(self, mock_projectile):
        mock_projectile.return_value = None
        self.assertTrue(self.player.shoot())
        self.assertEqual(self.player.ammo, 0)

    @patch('player.Player.shoot_projectile')
    def test_shooting_without(self, mock_projectile):
        mock_projectile.return_value = None
        self.player.ammo = 0
        self.assertFalse(self.player.shoot())
        self.assertEqual(self.player.ammo, 0)

    @patch('player.Player.shoot_projectile')
    def test_shooting_too_fast(self, mock_projectile):
        mock_projectile.return_value = None
        self.player.shot_cooldown = 100
        self.player.ammo = 2
        self.assertTrue(self.player.shoot())
        pygame.time.delay(50)
        self.assertFalse(self.player.shoot())
 
    @patch('player.Player.shoot_projectile')
    def test_shooting_on_time(self, mock_projectile):
        mock_projectile.return_value = None
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
        self.player.receive_key("somekey")
        self.assertEqual(len(self.player.keys), 1)
        self.assertTrue(self.player.keys.__contains__("somekey"))

    # Other stats

    def test_speed(self):
        self.assertEqual(self.player.speed, 3)

    # Input

    # This weird looking helper function exists because I found no other way to mock inputs
    # If I don't explicitly set everything as false, entering the control function will cause issues
    def get_all_false_keys(self):
        return {
            pygame.K_w: False,
            pygame.K_UP: False,
            pygame.K_s: False,
            pygame.K_DOWN: False,
            pygame.K_a: False,
            pygame.K_LEFT: False,
            pygame.K_d: False,
            pygame.K_RIGHT: False,
            pygame.K_LCTRL: False,
            pygame.K_RCTRL: False,
            pygame.K_LSHIFT: False,
            pygame.K_RSHIFT: False
        }

    @patch('pygame.key.get_pressed')
    @patch('player.Player.move_upwards')
    def test_up_key(self, mock_up, mock_key):
        self.key[pygame.K_w] = True
        mock_key.return_value = self.key
        mock_up.return_value = None
        self.player.control(mock_key.return_value)
        mock_up.assert_called_once() # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_called_once

    @patch('pygame.key.get_pressed')
    @patch('player.Player.move_downwards')
    def test_down_key(self, mock_down, mock_key):
        self.key[pygame.K_s] = True
        mock_key.return_value = self.key
        mock_down.return_value = None
        self.player.control(mock_key.return_value)
        mock_down.assert_called_once()

    @patch('pygame.key.get_pressed')
    @patch('player.Player.move')
    def test_left_key(self, mock_move, mock_key):
        self.key[pygame.K_a] = True
        mock_key.return_value = self.key
        mock_move.return_value = None
        self.player.direction.x = 0
        self.player.control(mock_key.return_value)
        self.assertAlmostEqual(self.player.direction.x,-1)

    @patch('pygame.key.get_pressed')
    @patch('player.Player.move')
    def test_right_key(self, mock_move, mock_key):
        self.key[pygame.K_d] = True
        mock_key.return_value = self.key
        mock_move.return_value = None
        self.player.direction.x = 0
        self.player.control(mock_key.return_value)
        self.assertAlmostEqual(self.player.direction.x,1)

    @patch('pygame.key.get_pressed')
    @patch('player.Player.shoot')
    def test_shoot_key(self, mock_shoot, mock_key):
        self.key[pygame.K_LCTRL] = True
        mock_key.return_value = self.key
        mock_shoot.return_value = None
        self.player.control(mock_key.return_value)
        mock_shoot.assert_called_once()

    @patch('pygame.key.get_pressed')
    def test_interact_key(self, mock_key):
        self.key[pygame.K_LSHIFT] = True
        mock_key.return_value = self.key
        self.player.interactive_mode = False
        self.player.control(mock_key.return_value)
        self.assertTrue(self.player.interactive_mode)