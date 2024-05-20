from youtube import youtube_api
from spotify import spotify_api
import discord
import asyncio
from song import songobj
class void_bot:
    def __init__(self,bot, guild) -> None:
        self.queue = []
        self.isPlaying = False
        self.voice_client = None
        self.guild = guild
        self.skip_flag = False
        self.bot = bot
        self.spapi = spotify_api()
        self.ytapi = youtube_api()
    
    def __repr__(self):
        return f"queue: {self.queue}, isPlaying: {self.isPlaying}, voice_client: {self.voice_client}, build: {self.guild}"

    async def add_to_queue(self, ctx, spotify_url):
        track_id = spotify_url.split("/")[-1]
        infos = await self.spapi.get_track_info(track_id)
        artists = [artist['name'] for artist in infos['artists']]
        track_name = infos['name']
        query = f"{track_name} {' '.join(artists)}"
        video_url, audio_url = await self.ytapi.get_track_url(query)
        song = songobj(audio_url, artists, track_name)
        self.queue.append(song)
        if len(self.queue) != 0:
            await ctx.send(f"Added {video_url} to queue")
        if not self.isPlaying:
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if len(self.queue) == 0:
            self.isPlaying = False
            if self.voice_client:
                await self.voice_client.disconnect()
                self.voice_client = None
            return
        self.isPlaying = True
        song_popped = self.queue.pop(0)
        await ctx.send(f"Now playing {song_popped.track_name} by {', '.join(song_popped.artists)}")
        if not self.voice_client or not self.voice_client.is_connected():
            self.voice_client = await ctx.author.voice.channel.connect()
        self.voice_client.play(discord.FFmpegPCMAudio(song_popped.audio_url), after=lambda e: self.bot.loop.create_task(self.song_finished(ctx)))
    async def song_finished(self, ctx):
        if not self.skip_flag:
            await self.play_next(ctx)
        else:
            self.skip_flag = False
    async def disconnect(self):
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None
            self.isPlaying = False
        self.queue.clear()
    async def skip(self, ctx):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            self.skip_flag = True
            await ctx.send("Skipping current song.")
            await self.play_next(ctx)


