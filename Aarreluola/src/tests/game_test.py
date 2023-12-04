import unittest
import pygame
import map
import game
import instance_loader
from renderer import Renderer
from player import Player
from gamestate import GameState
from enemy import load_enemy_types
from pickup import load_pickup_types
from game import load_campaign, get_level_tmx_file
from unittest.mock import patch

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        self.game_state.campaign_name = "unittestingCampaign"
        self.game_state.level_order = load_campaign(self.game_state)
        self.game_state.current_level = 0
        self.game_state.tmx_level = get_level_tmx_file(self.game_state.level_order[self.game_state.current_level],
                                                  self.game_state)

    def test_enemies_can_be_loaded (self):
        load_enemy_types()
        enemies = instance_loader.load_enemies_from_map(self.game_state.tmx_level)
        self.assertGreater(len(enemies),0)

    def test_pickups_can_be_loaded(self):
        load_pickup_types()
        pickups = instance_loader.load_pickups_from_map(self.game_state.tmx_level)
        self.assertGreater(len(pickups),0)

    def test_actions_and_zones_can_be_loaded(self):
        actions = instance_loader.load_actions_from_map(self.game_state.tmx_level)
        zones = instance_loader.load_zones_from_map(self.game_state.tmx_level,actions)
        self.assertGreater(len(actions),0)
        self.assertGreater(len(zones),0)

    def test_collisions_and_ladders_can_be_created (self):
        map.set_layers(self.game_state.tmx_level)
        map.create_collision_map(self.game_state.tmx_level)
        self.assertGreater(len(map.collision_map),0)

    @patch('renderer.Renderer.draw_message_screen')
    def test_everything_can_be_loaded_simultaneously (self, mock_msg):
        resolution = (1,1)
        self.game_state.renderer = Renderer(pygame.Surface(resolution),
                                            pygame.display.set_mode(resolution),
                                            resolution,
                                            1)
        mock_msg.return_value = None

        self.game_state.player = Player()
        game.load_level(self.game_state)

    @patch('game.handle_quit')
    @patch('renderer.Renderer.draw_message_screen')
    def test_next_level_does_not_load_if_flag_is_false (self, mock_msg, mock_quit):
        resolution = (1,1)
        self.game_state.renderer = Renderer(pygame.Surface(resolution),
                                            pygame.display.set_mode(resolution),
                                            resolution,
                                            1)
        mock_msg.return_value = None
        mock_quit.return_value = None

        self.game_state.flag_next_level = False
        self.game_state.player = Player()

        self.assertFalse(game.handle_next_level_flag(self.game_state))

    @patch('pygame.time.delay')
    @patch('game.handle_quit')
    @patch('renderer.Renderer.draw_message_screen')
    def test_next_level_loads_with_flag (self, mock_msg, mock_quit, mock_wait):
        resolution = (1,1)
        self.game_state.renderer = Renderer(pygame.Surface(resolution),
                                            pygame.display.set_mode(resolution),
                                            resolution,
                                            1)
        mock_wait.return_value = None
        mock_msg.return_value = None
        mock_quit.return_value = None

        self.game_state.flag_next_level = True
        self.game_state.player = Player()

        self.assertTrue(game.handle_next_level_flag(self.game_state))

    @patch('pygame.time.delay')
    @patch('game.handle_quit')
    @patch('renderer.Renderer.draw_message_screen')
    def test_player_spawns_after_death (self, mock_msg, mock_quit, mock_wait):
        resolution = (1,1)
        self.game_state.renderer = Renderer(pygame.Surface(resolution),
                                            pygame.display.set_mode(resolution),
                                            resolution,
                                            1)
        mock_wait.return_value = None
        mock_msg.return_value = None
        mock_quit.return_value = None

        self.game_state.flag_next_level = True
        self.game_state.player = Player()
        self.game_state.player.dead = True

        self.assertTrue(game.handle_player_status(self.game_state))

    @patch('pygame.time.delay')
    @patch('game.handle_quit')
    @patch('renderer.Renderer.draw_message_screen')
    def test_player_loses_after_death_if_no_lives (self, mock_msg, mock_quit, mock_wait):
        resolution = (1,1)
        self.game_state.renderer = Renderer(pygame.Surface(resolution),
                                            pygame.display.set_mode(resolution),
                                            resolution,
                                            1)
        mock_wait.return_value = None
        mock_msg.return_value = None
        mock_quit.return_value = True

        self.game_state.flag_next_level = True
        self.game_state.player = Player()
        self.game_state.player.life = 0
        self.game_state.player.dead = True

        self.assertTrue(game.handle_player_status(self.game_state))
        