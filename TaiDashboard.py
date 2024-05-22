from taipy import Gui
from bot_manager import bot_manager
from bot import void_bot

class Dashboard:
    def create_page(self, bots):
        # bots is a list, for each bot we need to extract guild, guild.id and isPlaying.
        # Create a data dictionary for the table
        data = {
            "guild": [bot.guild for bot in bots],
            "guild_id": [bot.guild.id for bot in bots],
            "isPlaying": [bot.isPlaying for bot in bots],
        }

        # Define the page with the table
        page = "<|{data}|table|>"
        
        # Run the GUI with the defined page
        return page
    
    def render_page(self, bots):
        page = self.create_page(bots)
        gui = Gui(page)
        gui.run(use_reloader=True)