from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class RemoveSongByIndex:
    def __init__(self, music_repository: MusicRepository):
        self.music_repository = music_repository

    def execute(self, server_id: str, index: int) -> Song:
        return self.music_repository.remove_song_by_index(server_id, index)