from re import split
import discord
from spotify import spotify_api
from youtube import youtube_api
from bot_manager import bot_manager
import secret
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='$', intents=intents)
bot_manager = bot_manager()
@bot.command()
async def manage_bot(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("This command must be used in a server")
        return
    #Create or get the instance of the bot
    music_bot = bot_manager.get_bot(guild)
    bot_manager.print_all_instances()
    await ctx.send(f"Bot instance for this guild: {music_bot}")



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
#spotify_api = spotify_api()
#youtube_api = youtube_api()
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
bot.run(secret.BOT_TOKEN)
#
