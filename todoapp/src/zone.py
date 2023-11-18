"""Zone contains Zone, conditions and all the child types of conditions"""
class Zone:
    """Zones are used to check for conditions. Default: Player inside."""
    def __init__(self, rect, additional_conditions, actions=[]):
        self.rect = rect
        self.conditions = [PlayerTouchingCondition(rect)]
        self.actions = actions
        if additional_conditions:
            self.conditions.extend(additional_conditions)

    def can_be_activated(self, player):
        """Check for conditions"""
        for condition in self.conditions:
            if not condition.check(player):
                return False
        return True

    def activate(self):
        """Execute any actions it contains, also receive any potential messages from them."""
        messages = []
        for action in self.actions:
            messages = action.execute()
        return messages


class Condition:
    """Parent class for handling conditions."""
    def check(self, player):
        """Checks whether the condition is fulfilled"""
        raise NotImplementedError(
            "I am not a condition. Use the proper ones below!")


class PlayerTouchingCondition(Condition):
    """Condition returns true if the player is within the zone"""
    def __init__(self, zone_rect):
        self.zone_rect = zone_rect

    def check(self, player):
        touching = player.get_rect().colliderect(self.zone_rect)
        return touching


class PlayerHasKeyCondition(Condition):
    """Condition return true if player has the right key."""
    def __init__(self, required_key):
        self.required_key = required_key

    def check(self, player):
        has_key = self.required_key in player.keys
        return has_key
