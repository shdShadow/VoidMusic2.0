import yt_dlp
import asyncio
import os
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
        info_dict = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(self.ydl_opts).extract_info(query, download=True))
        video_url = info_dict['entries'][0]['webpage_url']
        audio_url = info_dict['entries'][0]['url']
        return video_url, audio_url
    async def download_track(self, query, guild_id):
        folder_path = f'downloads/{guild_id}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch',
            'quiet': True,
            'outtmpl': f'{folder_path}/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # Use 320 kbps for high quality
            }],
        }
        loop = asyncio.get_event_loop()
        info_dict = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(query, download=True))
        
        # Extract the video URL
        video_url = info_dict['entries'][0]['webpage_url']
        
        # Format the output file path
        audio_file = f'{folder_path}/{info_dict["entries"][0]["id"]}.mp3'
        
        return video_url, audio_file


