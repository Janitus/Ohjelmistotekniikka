import unittest
import pygame
from enemy import Enemy
from unittest.mock import patch

class TestEnemy(unittest.TestCase):
    def setUp(self):
        surface = pygame.Surface((1, 1))
        surface.fill((255, 255, 255))
        self.enemy = Enemy(surface)

    def test_enemy_can_die(self):
        self.enemy.die()
        self.assertTrue(self.enemy.dead, True)

    @patch('character.get_collision_by_coordinate')
    @patch('enemy.Enemy.is_facing_a_fall')
    def test_enemy_changes_direction_if_fall(self, mock_fall, mock_collision):
        mock_collision.return_value = False
        mock_fall.return_value = True
        self.enemy.avoid_falls = True

        old_dir = self.enemy.direction
        old_dir.x *= -1

        self.enemy.patrol()
        self.assertEqual(self.enemy.direction,old_dir)

    @patch('character.get_collision_by_coordinate')
    @patch('enemy.Enemy.is_facing_a_fall')
    def test_enemy_does_not_change_direction_if_no_fall(self, mock_fall, mock_collision):
        mock_collision.return_value = False
        mock_fall.return_value = False
        self.enemy.avoid_falls = True

        old_dir = self.enemy.direction

        self.enemy.patrol()
        self.assertEqual(self.enemy.direction,old_dir)

    @patch('character.get_collision_by_coordinate')
    def test_enemy_changes_direction_if_collision(self, mock_collision):
        mock_collision.return_value = True
        self.enemy.avoid_falls = False

        old_dir = self.enemy.direction
        old_dir.x *= -1

        self.enemy.patrol()
        self.assertEqual(self.enemy.direction,old_dir)

    @patch('enemy.get_collision')
    def test_enemy_detects_floor_on_left(self, mock_collision):
        mock_collision.return_value = True
        self.assertFalse(self.enemy.is_facing_a_fall())
        
    @patch('enemy.get_collision')
    def test_enemy_detects_floor_on_right(self, mock_collision):
        mock_collision.return_value = True
        self.enemy.direction.x *= -1
        self.assertFalse(self.enemy.is_facing_a_fall())

    @patch('enemy.get_collision')
    def test_enemy_detects_falls_on_right(self, mock_collision):
        mock_collision.return_value = False
        self.enemy.direction.x *= -1
        self.assertTrue(self.enemy.is_facing_a_fall())
