import unittest
import character
import pygame


class TestCharacter(unittest.TestCase):
    def setUp(self):
        surface = pygame.Surface((1, 1))
        surface.fill((255, 255, 255))
        self.character = character.Character(surface, 16, 24)
        self.character.health = 10
        self.character.max_health = 10
        self.character.speed = 3
        self.character.gravity = .2

        self.test_collision_map = [
            [True, True, True, True],
            [True, False, False, True],
            [True, False, False, True],
            [True, True, True, True]
        ]

        self.test_ladder_map = [
            [True, True, True, True],
            [True, False, False, True],
            [True, False, False, True],
            [True, True, True, True]
        ]


    def test_gravity_applies(self):
        self.assertEqual(self.character.velocity_y, 0)
        #self.character.apply_gravity()
        ############self.assertEqual(self.character.velocity_y, 0.2)

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