"""Actions to make certain events happen"""
class Action:
    """Actions are events that occur in the game after being triggered by zones"""
    def __init__(self, action_id=None):
        self.action_id = action_id
        self.use_count = 0
        self.use_limit = 1

    def execute(self):
        """Execute is a method that is called when some condition(s) are fulfilled"""
        if self.use_count >= self.use_limit:
            return False
        self.use_count += 1
        return True



class DestroyAction(Action):
    """Destroys a position in the environment layer when executed"""
    def __init__(self, action_id, position):
        super().__init__(action_id)
        self.position = position

    def execute(self):
        if not super().execute():
            return False
        # Generated solution to avoid circular import. Might want to refactor the code later.
        from map import destroy_block
        destroy_block(*self.position)
        # End gen
        return self.position


class ExitAction(Action):
    """Signals exit so that the game will load the next level"""
    def execute(self):
        if not super().execute():
            return False
        return "exit"
