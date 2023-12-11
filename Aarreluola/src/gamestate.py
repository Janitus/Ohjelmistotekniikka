from dataclasses import dataclass

@dataclass
class GameState:
    """Game state is used to encapsulate information"""
    campaign_name = "testCampaign"
    tmx_level = None
    current_level = 0
    level_order = None
    flag_next_level = False

    pickups = []
    zones = None
    enemies = []
    projectile_manager = None
    lighting = None
    renderer = None

    stats = None
    player = None
