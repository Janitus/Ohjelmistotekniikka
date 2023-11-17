import unittest
import player
import game
import pygame


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = game.main
        self.player = player.Player(*game.load_player())
        self.player.width = 16
        self.player.height = 24
        self.player.life = 3
        self.player.speed = 3



    def test_max_hp(self):
        self.assertEqual(self.player.max_health, 10)
