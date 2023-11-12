class Zone:
    def __init__(self, rect, additional_conditions, actions=[]):
        self.rect = rect
        self.conditions = [PlayerTouchingCondition(rect)]
        self.actions = actions
        if additional_conditions: self.conditions.extend(additional_conditions)

    def is_activated(self, player):
        for condition in self.conditions:
            if not condition.check(player):
                #print(f"Condition {condition} failed for player {player}")
                return False
        return True
    
    def activate(self):
        messages = []
        for action in self.actions:
            messages = action.execute()
        return messages


class Condition:
    def check(self, player):
        raise NotImplementedError("I am not a condition. Use the proper ones below!")

class PlayerTouchingCondition(Condition):
    def __init__(self, zone_rect):
        self.zone_rect = zone_rect

    def check(self, player):
        touching = player.get_rect().colliderect(self.zone_rect)
        #print(f"PlayerTouchingCondition: {touching}, Player: {player.get_rect()}, Zone: {self.zone_rect}")
        return touching

class PlayerHasKeyCondition(Condition):
    def __init__(self, required_key):
        self.required_key = required_key

    def check(self, player):
        has_key = self.required_key in player.keys
        #print(f"PlayerHasKeyCondition: {has_key}, Player Keys: {player.keys}, Required: {self.required_key}")
        return has_key
    
    