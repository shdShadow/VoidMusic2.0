import logging
from logging.handlers import RotatingFileHandler
import os
from youtube import youtube_api
from spotify import spotify_api
import discord
import asyncio
from song import songobj

class void_bot:
    def __init__(self, bot, guild) -> None:
        self.queue = []
        self.isPlaying = False
        self.voice_client = None
        self.guild = guild
        self.skip_flag = False
        self.bot = bot
        self.spapi = spotify_api()
        self.ytapi = youtube_api()
        self.setup_logger()
        self.logger.info(f"Created bot instance for guild: {guild.name} (ID: {guild.id})")

    def setup_logger(self):
        log_directory = 'logs'
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        log_file = os.path.join(log_directory, f'bot_{self.guild.id}.log')
        self.logger = logging.getLogger(f'bot_{self.guild.id}')
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=1)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    async def add_to_queue_youtube(self, ctx, query):
        self.logger.info(f"User: {ctx.author.name} used command: $play_youtube with query: {query}")
        audio_file, video_title = await self.ytapi.download_audio_youtube(query, self.guild)
        song = songobj(audio_file, None, None, ctx, video_title)
        self.logger.info(f"Added {video_title} to bot queue")
        self.queue.append(song)
        if len(self.queue) != 0:
            await ctx.send(f"Added {query} to queue")
        if not self.isPlaying:
            await self.play_next(ctx)

    async def add_to_queue_query(self, ctx, query):
        self.logger.info(f"User: {ctx.author.name} used command $play with query: {query}")
        video_url, audio_file, video_title = await self.ytapi.download_track(query, self.guild)
        song = songobj(audio_file, None, None, ctx, video_title)
        self.logger.info(f"Added {video_title} to bot queue")
        self.queue.append(song)
        if len(self.queue) != 0:
            await ctx.send(f"Added {video_url} to queue")
        if not self.isPlaying:
            await self.play_next(ctx)

    async def add_to_queue_spotify(self, ctx, spotify_url):
        self.logger.info(f"User: {ctx.author.name} used command: $play_spotify with query: {query}")
        track_id = spotify_url.split("/")[-1]
        infos = await self.spapi.get_track_info(track_id)
        self.logger.info(f"Called spotify api correctly")
        artists = [artist['name'] for artist in infos['artists']]
        track_name = infos['name']
        query = f"{track_name} {' '.join(artists)}"
        video_url, audio_file, video_title = await self.ytapi.download_track(query, self.guild)
        song = songobj(audio_file, artists, track_name, ctx, video_title)
        self.logger.info(f"Added {video_title} to bot queue")
        self.queue.append(song)
        if len(self.queue) != 0:
            await ctx.send(f"Added {video_url} to queue")
        if not self.isPlaying:
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if len(self.queue) == 0:
            self.logger.info(f"Bot queue is empty. The bot will soon leave")
            self.isPlaying = False
            if self.voice_client:
                await self.voice_client.disconnect()
                self.logger.info(f"Bot disconnect from voice channel")
                self.voice_client = None
            return
        self.isPlaying = True
        song_popped = self.queue.pop(0)
        self.logger.info(f"Bot popped first element from queue. Title:{song_popped.video_title} ")
        await ctx.send(f"Now playing {song_popped.video_title}")
        if not self.voice_client or not self.voice_client.is_connected():
            self.logger.info(f"The bot is not connected to voice channel. It will soon")
            self.voice_client = await ctx.author.voice.channel.connect()
        self.logger.info(f"Bot is starting ffmpeg stream for popped song")
        self.voice_client.play(discord.FFmpegPCMAudio(song_popped.audio_file), after=lambda e: self.bot.loop.create_task(self.song_finished(ctx)))

    async def song_finished(self, ctx):

        if not self.skip_flag:
            await self.play_next(ctx)
        else:
            self.skip_flag = False

    async def disconnect(self, ctx):
        self.logger.info(f"User: {ctx.author.name} used command $disconnect")
        if self.voice_client:
            self.logger.info(f"The bot is in a voice channel. Disconnecting now")
            await self.voice_client.disconnect()
            self.voice_client = None
            self.isPlaying = False
        self.logger.info(f"Cleaning downloads directory for server: {self.guild}")
        self.queue.clear()
        self.cleanup_files()

    async def skip(self, ctx):
        self.logger.info("Bot is skipping current song")
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            self.skip_flag = True
            await ctx.send("Skipping current song.")
            await self.play_next(ctx)

    def cleanup_files(self):
        guild_folder = f'downloads/{self.guild}'
        self.logger.info(f"Cleaning up file directory for server: {self.guild}")
        if os.path.exists(guild_folder):
            for file_name in os.listdir(guild_folder):
                file_path = os.path.join(guild_folder, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

    async def pause(self, ctx):
        self.logger.info(f"User: {ctx.author.name} used command $pause")
        if self.voice_client.is_playing():
            self.voice_client.pause()
            self.logger.info(f"Bot was playing. Stopping playback")
            await ctx.send("Playback paused.")
        else:
            await ctx.send("No audio is currently playing.")

    async def resume(self, ctx):
        self.logger.info(f"User: {ctx.author.name} used command $resume")
        if self.voice_client.is_paused():
            self.voice_client.resume()
            self.logger.info(f"Bot was stopped. Resuming playback")
            await ctx.send("Playback resumed.")
        else:
            await ctx.send("No audio is currently paused.")

    def get_status(self):
        if self.voice_client and self.voice_client.is_connected():
            return "Connected"
        return "Disconnected"
