from bot import void_bot

class bot_manager:
    def __init__(self):
        self.bots = {}

    def get_bot(self, bot,guild):
        if guild.id not in self.bots:
            self.bots[guild.id] = void_bot(bot, guild)
        return self.bots[guild.id]
    def print_all_instances(self):
        for instance in self.bots.values():
            print(instance)
    def remove_bot(self, guild):
        if guild in self.bots:
            del self.bots[guild]
    def get_bot_instance(self, guild):
        if guild.id not in self.bots:
            return None
        return self.bots[guild.id]

