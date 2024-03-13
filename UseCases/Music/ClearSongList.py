from Repository.Music.MusicRepository import MusicRepository

class ClearSongList:
    def __init__(self, music_repository: MusicRepository):
        self.music_repository = music_repository

    def execute(self, server_id: str):
        self.music_repository.clear_song_list(server_id)