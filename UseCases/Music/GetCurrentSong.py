from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class GetCurrentSong:
    def __init__(self, music_repository: MusicRepository):
        self.music_repository = music_repository

    def execute(self, server_id: str) -> Song:
        return self.music_repository.get_current_song(server_id)