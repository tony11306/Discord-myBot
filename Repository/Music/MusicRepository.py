from typing import Dict, List

from Model.Song import Song

class MusicRepository:
    def __init__(self):
        self.server_song_list_map: Dict[str, List] = {}

    def get_current_song(self, server_id: str) -> Song:
        song_list = self.server_song_list_map.get(server_id, None)

        if song_list:
            return song_list[0]
        return None
    
    def get_song_list(self, server_id: str) -> List[Song]:
        return self.server_song_list_map.get(server_id, [])
    
    def get_song_list_range(self, server_id: str, start: int, end: int) -> List[Song]:
        song_list = self.server_song_list_map.get(server_id, [])
        return song_list[start:end]
    
    def remove_current_song(self, server_id: str):
        self.remove_song_by_index(server_id, 0)
    
    def clear_song_list(self, server_id: str):
        self.server_song_list_map.pop(server_id, None)

    def add_song(self, server_id: str, song: Song):
        song_list = self.server_song_list_map.get(server_id, None)

        if song_list:
            song_list.append(song)
        else:
            self.server_song_list_map[server_id] = [song]
    
    def remove_song_by_index(self, server_id: str, index: int) -> Song:
        song_list = self.server_song_list_map.get(server_id, None)
        song = None
        if song_list and len(song_list) > index and index >= 0:
            song = song_list.pop(index)
            if len(song_list) == 0:
                self.server_song_list_map.pop(server_id, None)
        return song
        
    