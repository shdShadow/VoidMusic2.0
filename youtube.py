import yt_dlp
import asyncio

class youtube_api:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch',
            'quiet': True,
        }

    async def get_track_url(self, query):
        loop = asyncio.get_event_loop()
        info_dict = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(self.ydl_opts).extract_info(query, download=False))
        video_url = info_dict['entries'][0]['webpage_url']
        audio_url = info_dict['entries'][0]['url']
        return video_url, audio_url
