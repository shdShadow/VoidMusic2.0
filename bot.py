class void_bot:

    def __init__(self, guild) -> None:
        self.queue = []
        self.isPlaying = False
        self.voice_client = None
        self.guild = guild

    def __repr__(self):
        return f"queue: {self.queue}, isPlaying: {self.isPlaying}, voice_client: {self.voice_client}, build: {self.guild}"
