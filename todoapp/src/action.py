"""Actions to make certain events happen"""
class Action:
    """Actions are events that occur in the game after being triggered by zones. Example: DestroyAction contains a position of the environment to destroy."""
    def __init__(self, id=None):
        self.id = id
        self.use_count = 0
        self.use_limit = 1

    def execute(self):
        """Execute is a method that is called when a zone fulfills all of it's conditions. When execute is called, the action will be completed"""
        if self.use_count >= self.use_limit:
            return False
        self.use_count += 1
        return True



class DestroyAction(Action):
    """Destroys a position in the environment layer when executed"""
    def __init__(self, id, position):
        super().__init__(id)
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
