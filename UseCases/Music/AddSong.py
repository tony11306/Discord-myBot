from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class AddSong:
    def __init__(self, music_repository: MusicRepository):
        self.music_repository = music_repository

    def execute(self, server_id: str, song: Song):
        self.music_repository.add_song(server_id, song)