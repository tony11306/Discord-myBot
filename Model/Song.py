class Song:
    def __init__(self, title: str, duration: int, thumbnail: str, uploader: str, audio_url: str, webpage_url: str, requester_id: str):
        self.title = title
        self.duration = duration
        self.thumbnail = thumbnail
        self.uploader = uploader
        self.audio_url = audio_url
        self.webpage_url = webpage_url
        self.requester_id = requester_id

    def duration_in_minutes_notation(self) -> str:
        if self.duration < 0:
            return "直播中"
        return f"{self.duration // 60}:{self.duration % 60:02d}"