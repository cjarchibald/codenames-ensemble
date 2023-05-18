import copy

class BotObjects():
    def __init__(self, bot_objects_arg):
        self.bot_objects_arg = bot_objects_arg

    def get_bot_object_copy(self, bot_constructor_key):
        return copy.deepcopy(self.bot_objects_arg[bot_constructor_key])