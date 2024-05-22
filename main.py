from re import split
import threading
import discord
from spotify import spotify_api
from youtube import youtube_api
from bot_manager import bot_manager
import secret
from discord.ext import commands
import json
from taipy import Gui
from flask import Flask, render_template, jsonify, url_for
import asyncio
import os
intents = discord.Intents.default()
intents.voice_states = True
spotify_api = spotify_api()
bot = commands.Bot(command_prefix='$', intents=intents)
bot_manager = bot_manager()

@bot.command()
async def manage_bot(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    #Create or get the instance of the bot
    music_bot = bot_manager.get_bot_instance(guild)
    if music_bot is None:
        await ctx.send("There is no bot instance for this guild")
        return
    await ctx.send(f"Bot instance for this guild: {music_bot}")
@bot.command()
async def play_youtube(ctx, *, query):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot(bot, guild)
    stripped_text = query.split('>', 1)[-1].strip()
    await music_bot.add_to_queue_youtube(ctx, stripped_text)
@bot.command()
async def play(ctx, *, query):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot(bot, guild)
    stripped_text = query.split('>', 1)[-1].strip()
    await music_bot.add_to_queue_query(ctx, stripped_text)
@bot.command()
async def play_spotify(ctx, *, spotify_url):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot(bot, guild)
    await music_bot.add_to_queue_spotify(ctx, spotify_url)
@bot.command()
async def debug_queue(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot(bot,guild)
    await ctx.send(f"Queue: {music_bot.queue}")
@bot.command()
async def pause(ctx):
    guild= ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot_instance(guild)
    if music_bot is None:
        await ctx.send("There is no bot instance for this guild")
        return
    await music_bot.pause(ctx)
    await ctx.send("Playback paused")
    
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot and (member.voice is None or member.voice.channel is None):
        guild = member.guild
        music_bot = bot_manager.get_bot(bot, guild)
        await music_bot.disconnect()
        bot_manager.remove_bot(guild.id)  

@bot.command()
async def disconnect(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot_instance(guild)
    if music_bot is None:
        await ctx.send("There is no bot instance for this guild")
        return
    await music_bot.disconnect()
    bot_manager.remove_bot(guild.id)
    await ctx.send("Disconnected from voice channel")

@bot.command()
async def skip(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot_instance(guild)
    if music_bot is None:
        await ctx.send("There is no bot instance for this guild")
        return
    await music_bot.skip(ctx)
@bot.command()
async def resume(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    music_bot = bot_manager.get_bot_instance(guild)
    if music_bot is None:
        await ctx.send("There is no bot instance for this guild")
        return
    await music_bot.resume(ctx)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
#@bot.command()
#async def play_spotify(ctx, *, spotify_url):
#    # Check if the user is in a voice channel
#    print(ctx)
#    if ctx.author.voice is None or ctx.author.voice.channel is None:
#        await ctx.send("You need to be in a voice channel to use this command!")
#        return
#    
#    # Get the voice channel of the user
#    voice_channel = ctx.author.voice.channel
#    """
#        https://open.spotify.com/track/7DkN4oeXv2mqyPy0sJNrus
#    """
#    track_id = spotify_url.split("/")[-1]
#    infos = spotify_api.get_track_info(track_id)
#    # Connect to the voice channel
#    voice_client = await voice_channel.connect()
#    print(json.dumps(infos, indent=4))
#    artists = []
#    track_name = ""
#    for artist in infos['artists']:
#        artists.append(artist['name'])
#    track_name = infos['name']
#    youtube_api.get_track_url(artists, track_name)
#    await ctx.send(f"Joined {voice_channel}, now playing {track_name} by {', '.join(artists)}")
#
#@bot.event
#async def on_ready():
#    print(f'Logged in as {bot.user}')
#
#given the bot list, extract guild, guild.id and isPLaying and create a table

app = Flask(__name__)

data = {
    "columns": ["Guild", "Guild ID", "Is Playing", "Logs"],
    "rows": []
}

def update_data(bot_manager):
    global data
    bots_list = bot_manager.bots.values()
    data["rows"] = [
        {
            "Guild": bot.guild.name,
            "Guild ID": bot.guild.id,
            "Playing": "Playing" if bot.isPlaying else "Stopped",
            "Logs": url_for('view_logs', guild_id=bot.guild.id),
        }
        for bot in bots_list
    ]

@app.route('/')
def index():
    update_data(bot_manager)
    return render_template('index.html', data=data)

@app.route('/data')
def get_data():
    update_data()
    return jsonify(data)
@app.route('/logs/<int:guild_id>')
def view_logs(guild_id):
    log_file = f'logs/bot_{guild_id}.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            logs = file.read()
        return f'<pre>{logs}</pre>'
    else:
        return 'No logs available for this bot.', 404
# Run Flask app in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Start the Flask app and the Discord bot
def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(bot.start(secret.BOT_TOKEN))

if __name__ == "__main__":
    main()

