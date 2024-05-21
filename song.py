class songobj:
    def __init__(self, audio_file, artists, track_name, ctx, video_title) -> None:
        self.audio_file = audio_file
        self.artists = artists
        self.track_name = track_name
        self.ctx = ctx
        self.video_title = video_title