from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song

class ContinueOutputPort:
    def continue_playing(self, server_id: str):
        raise NotImplementedError

class Continue:
    def __init__(self, output_port: ContinueOutputPort=None):
        self.output_port = output_port

    def execute(self, server_id: str):
        self.output_port.continue_playing(server_id)