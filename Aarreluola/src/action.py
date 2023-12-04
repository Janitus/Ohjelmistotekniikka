"""Actions to make certain events happen"""
class Action:
    """Actions are events that occur in the game after being triggered by zones"""
    def __init__(self, action_id=None):
        self.action_id = action_id
        self.use_count = 0
        self.use_limit = 1
        self.state = None

    def execute(self, game_state = None):
        """Execute is a method that is called when some condition(s) are fulfilled"""
        self.state = game_state
        if self.use_count >= self.use_limit:
            return False
        self.use_count += 1
        return True



class DestroyAction(Action):
    """Destroys a position in the environment layer when executed"""
    def __init__(self, action_id, position):
        super().__init__(action_id)
        self.position = position

    def execute(self, game_state = None):
        self.state = game_state
        if not super().execute():
            return False
        # Generated solution to avoid circular import. Might want to refactor the code later.
        from map import destroy_block
        destroy_block(*self.position)
        # End gen
        return self.position


class ExitAction(Action):
    """Signals exit so that the game will load the next level"""
    def execute(self, game_state = None):
        self.state = game_state
        if not super().execute():
            return False
        return "exit"

class DamageAction(Action):
    """Deals damage to the player"""
    def __init__(self, action_id, damage, knockup):
        super().__init__(action_id)
        self.use_limit = float('inf')
        self.damage = damage
        self.knockup = knockup

    def execute(self, game_state=None):
        if game_state is not None and super().execute():
            game_state.player.damage(self.damage, self.knockup)

class KnockupAction(Action):
    """Knocks the player up player"""
    def __init__(self, action_id, knockup):
        super().__init__(action_id)
        self.use_limit = float('inf')
        self.knockup = knockup

    def execute(self, game_state=None):
        if game_state is not None and super().execute():
            game_state.player.knock_up(self.knockup)
