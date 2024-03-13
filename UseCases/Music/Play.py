from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class PlayOutputPort:
    def play(self, server_id: str, song: Song):
        raise NotImplementedError

class Play:
    def __init__(self, music_repository: MusicRepository, output_port: PlayOutputPort=None):
        self.music_repository = music_repository
        self.output_port = output_port

    def execute(self, server_id: str):
        current_song = self.music_repository.get_current_song(server_id)
        
        if self.output_port:
            self.output_port.play(server_id, current_song)