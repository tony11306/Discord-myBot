from typing import List

from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class GetSongList:
    def __init__(self, music_repository: MusicRepository):
        self.music_repository = music_repository

    def execute(self, server_id: str, page: int=None) -> List[Song]:
        if page is None:
            return self.music_repository.get_song_list(server_id)

        return self.music_repository.get_song_list_range(server_id, (page-1) * 10, (page) * 10)