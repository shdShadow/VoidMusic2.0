import yt_dlp
class youtube_api:
    

    async def get_track_url(query):
        ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=False)
            video_url = info_dict['entries'][0]['webpage_url']
            return video_url