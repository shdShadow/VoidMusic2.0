from youtube import youtube_api
from spotify import spotify_api
class void_bot:
    def __init__(self, guild) -> None:
        self.queue = []
        self.isPlaying = False
        self.voice_client = None
        self.guild = guild
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
        video_url = await youtube_api.get_track_url(query)
        self.queue.append(video_url)
        await ctx.send(f"Added {video_url} to queue")

