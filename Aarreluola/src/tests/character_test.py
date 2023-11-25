import unittest
import character
import pygame
from unittest.mock import patch # https://www.youtube.com/watch?v=ClAdw7ZJf5E


class TestCharacter(unittest.TestCase):
    def setUp(self):
        surface = pygame.Surface((1, 1))
        surface.fill((255, 255, 255))
        self.character = character.Character(surface, 16, 24)
        self.character.health = 10
        self.character.max_health = 10
        self.character.speed = 3
        self.character.gravity = .2


    @patch('character.get_collision_by_coordinate')
    def test_can_collide(self, mock_get_collision):
        mock_get_collision.return_value = True
        self.assertTrue(self.character.collides(1, 1))
        self.assertTrue(self.character.collides(-1, 1))
        self.assertTrue(self.character.collides(1, -1))
        self.assertTrue(self.character.collides(-1, -1))

    @patch('character.get_collision_by_coordinate')
    def test_can_not_collide_without_collision(self, mock_get_collision):
        mock_get_collision.return_value = False
        self.assertFalse(self.character.collides(1, 1))
        self.assertFalse(self.character.collides(-1, 1))
        self.assertFalse(self.character.collides(1, -1))
        self.assertFalse(self.character.collides(-1, -1))
        self.assertFalse(self.character.collides(0, 1))

    @patch('character.get_collision_by_coordinate')
    @patch('character.Character.can_climb')
    def test_can_climb_up(self, mock_can_climb, mock_get_collision):
        mock_can_climb.return_value = True
        mock_get_collision.return_value = False

        old_position = self.character.position
        old_position[1] += self.character.speed
        self.character.move_upwards()
        self.assertEqual(self.character.position,old_position)

    @patch('character.get_collision_by_coordinate')
    @patch('character.Character.can_climb')
    def test_can_climb_down(self, mock_can_climb, mock_get_collision):
        mock_can_climb.return_value = True
        mock_get_collision.return_value = False

        old_position = self.character.position
        old_position[1] -= self.character.speed
        self.character.move_downwards()
        self.assertEqual(self.character.position,old_position)

        mock_can_climb.return_value = False
        old_position = self.character.position
        self.character.move_downwards()
        self.assertEqual(self.character.position,old_position)

    @patch('character.get_collision_by_coordinate')
    @patch('character.get_ladder_by_coordinate')
    def test_will_climb_with_ladder(self, mock_get_ladder, mock_get_collision):
        mock_get_ladder.return_value = True
        mock_get_collision.return_value = False
        self.assertTrue(self.character.can_climb())

        old_position = self.character.position
        old_position[1] += self.character.speed
        self.character.move_upwards()
        self.assertEqual(self.character.position,old_position)
        

    @patch('character.Character.feet_on_ground')
    @patch('character.get_ladder_by_coordinate')
    def test_will_jump_without_ladder_if_feet_on_ground (self, mock_get_ladder, mock_get_feet_on_ground):
        mock_get_ladder.return_value = False
        mock_get_feet_on_ground.return_value = True
        self.assertFalse(self.character.can_climb())
        self.character.move_upwards()
        self.assertEqual(self.character.velocity_y, -self.character.jump_power)

    @patch('character.Character.feet_on_ground')
    @patch('character.get_ladder_by_coordinate')
    def test_will_not_jump_if_feet_on_ground (self, mock_get_ladder, mock_get_feet_on_ground):
        mock_get_ladder.return_value = False
        mock_get_feet_on_ground.return_value = False
        self.assertFalse(self.character.can_climb())
        self.character.move_upwards()
        self.assertEqual(self.character.velocity_y, 0)

    @patch('character.get_collision_by_coordinate')
    def test_can_have_feet_on_ground (self, mock_get_collision):
        mock_get_collision.return_value = True
        self.assertTrue(self.character.feet_on_ground())

    @patch('character.get_collision_by_coordinate')
    def test_can_not_have_feet_on_ground (self, mock_get_collision):
        mock_get_collision.return_value = False
        self.assertFalse(self.character.feet_on_ground())

    @patch('character.Character.can_climb')
    def test_gravity_does_not_apply_when_on_ladder(self, mock_can_climb):
        mock_can_climb.return_value = True
        self.character.update()
        self.assertEqual(self.character.velocity_y, 0)

    @patch('character.get_collision_by_coordinate')
    @patch('character.Character.can_climb')
    def test_gravity_applies (self, mock_can_climb, mock_get_collision):
        mock_get_collision.return_value = False
        mock_can_climb.return_value = False
        self.character.update()
        self.assertEqual(self.character.velocity_y, self.character.gravity)


    @patch('character.get_collision_by_coordinate')
    def test_can_not_move_if_collision (self, mock_get_collision):
        mock_get_collision.return_value = True
        old_pos = self.character.position
        self.character.move(self.character.speed, self.character.speed)
        self.assertEqual(self.character.position, old_pos)

    def test_zero_damage_does_not_affect_invulnerability(self):
        last_hit = self.character.last_hit
        self.character.damage(0)
        self.assertEqual(self.character.last_hit, last_hit)

    def test_negative_healing_does_not_affect_health(self):
        self.character.heal(-5)
        self.assertEqual(self.character.health, 10)

    def test_knock_up_affects_y_velocity(self):
        self.character.knock_up(5)
        self.assertEqual(self.character.velocity_y, -5)

    def test_character_can_die(self):
        self.character.die()
        self.assertTrue(self.character.dead, True)

    def test_center_position_is_correct(self):
        self.assertEqual(self.character.center()[1], self.character.position[1]-self.character.height/2)
        self.assertEqual(self.character.center()[0], self.character.position[0])
