class Action:
    def __init__(self, id=None):
        self.id = id
        self.use_count = 0
        self.use_limit = 1

    def execute(self):
        if self.use_count >= self.use_limit:
            return False
        self.use_count += 1
        return True


class DestroyAction(Action):
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
    def execute(self):
        if not super().execute():
            return False
        return "exit"
