import yt_dlp
from typing import List
import concurrent.futures
import asyncio
import re
import requests

from Repository.Music.MusicRepository import MusicRepository
from Model.Song import Song
from Config import YT_DLP_SERVER_URL

class SearchYoutubeSong:
    def __init__(self):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.url_regex = re.compile(r'https?://(www\.)?youtube\..+')
        self.playlist_url_regex = re.compile(r'https?://(www\.)?youtube\..+/playlist\?.+')
        self.youtube_song_name_search_handler = YoutubeSongNameSearchHandler()
        self.youtube_song_url_search_handler = YoutubeSongUrlSearchHandler(self.youtube_song_name_search_handler)
        self.youtube_playlist_search_handler = YoutubePlayListSearchHandler(self.youtube_song_url_search_handler)
        self.first_handler: SearchHandler = self.youtube_playlist_search_handler


    async def execute(self, requester_id: str, song_name: str=None) -> List[Song]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, self.first_handler.search, requester_id, song_name)

class SearchHandler:
    def __init__(self, next_handler: 'SearchHandler'=None) -> None:
        self.next_handler = next_handler
    
    def search(self, requester_id: str, keyword) -> List[Song]:
        if self.next_handler is None:
            return []
        return self.next_handler.search(requester_id, keyword)
    
class YoutubePlayListSearchHandler(SearchHandler):
    def __init__(self, next_handler: SearchHandler=None) -> None:
        self.playlist_url_regex = re.compile(r'https?://(www\.)?youtube\..+/playlist\?.+')
        super().__init__(next_handler)
    
    def search(self, requester_id: str, keyword) -> List[Song]:
        if self.playlist_url_regex.match(keyword):
            info = requests.post(f'{YT_DLP_SERVER_URL}/songs',
                                    json={'query': keyword}).json()
            songs = []
            for entry in info['entries']:
                song = Song(
                    title=entry['title'],
                    audio_url=None,
                    thumbnail=entry['thumbnails'][0],
                    duration=entry['duration'],
                    uploader=entry['uploader'],
                    webpage_url=entry['url'],
                    requester_id=requester_id
                )
                songs.append(song)
            return songs
        return super().search(requester_id, keyword)

class YoutubeSongUrlSearchHandler(SearchHandler):
    def __init__(self, next_handler: SearchHandler=None) -> None:
        self.url_regex = re.compile(r'https?://(www\.)?youtube\..+watch\?.+')
        super().__init__(next_handler)
    
    def search(self, requester_id: str, keyword) -> List[Song]:
        if self.url_regex.match(keyword):
            if '&list=' in keyword:
                keyword = keyword.split('&list=')[0]
            info = requests.post(f'{YT_DLP_SERVER_URL}/songs',
                                    json={'query': keyword}).json()
            song = Song(
                title=info.get('title', None),
                audio_url=info.get('url', None),
                thumbnail=info.get('thumbnail', None),
                duration=info.get('duration', -1),
                uploader=info.get('uploader', None),
                webpage_url=info.get('webpage_url', None),
                requester_id=requester_id
            )
            return [song]
        return super().search(requester_id, keyword)
    
class YoutubeSongNameSearchHandler(SearchHandler):
    def __init__(self, next_handler: SearchHandler=None) -> None:
        super().__init__(next_handler)

    def search(self, requester_id: str, keyword) -> List[Song]:
        info = requests.post(f'{YT_DLP_SERVER_URL}/songs',
                                json={'query': keyword}).json()
        try:
            if info['entries']:
                song_info = info['entries'][0]
                song = Song(
                    title=song_info['title'],
                    audio_url=song_info['url'],
                    thumbnail=song_info['thumbnail'],
                    duration=song_info.get('duration', -1),
                    uploader=song_info['uploader'],
                    webpage_url=song_info['webpage_url'],
                    requester_id=requester_id
                )
                return [song]
        except Exception as e:
            return super().search(requester_id, keyword)