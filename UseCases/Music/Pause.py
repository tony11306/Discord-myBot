from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class PauseOutputPort:
    def pause(self, server_id: str, song: Song):
        raise NotImplementedError

class Pause:
    def __init__(self, music_repository: MusicRepository, output_port: PauseOutputPort=None):
        self.music_repository = music_repository
        self.output_port = output_port

    def execute(self, server_id: str):
        current_song = self.music_repository.get_current_song(server_id)
        if current_song is None:
            raise ValueError("No song is currently playing")
        
        if self.output_port:
            self.output_port.pause(server_id, current_song)
        