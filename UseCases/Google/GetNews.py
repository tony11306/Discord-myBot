import requests
from bs4 import BeautifulSoup
from typing import List
import urllib.parse

class GoogleNews:
    def __init__(self, title: str, link: str, time: str, media: str):
        self.title: str = title
        self.link: str = link
        self.time: str = time
        self.media: str = media

class GetNews:
    def __init__(self):
        pass

    def execute(self, news_search: str, count: int=10) -> List[GoogleNews]:
        news_url = f'https://news.google.com/search?q={urllib.parse.quote(news_search)}&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
        res = requests.get(news_url)
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.find_all('a', class_='JtKRv')
        media = soup.find_all('div', class_='vr1PYe')
        timeAgo = soup.find_all('time', class_='hvbAAd')

        news_list = []
        i = 0
        while i < count:
            try:
                news = GoogleNews(title[i].text, title[i]['href'], timeAgo[i].text, media[i].text)
                if self._check_if_too_long(news):
                    i += 1
                    continue
                news_list.append(GoogleNews(title[i].text, 'https://news.google.com/' + title[i]['href'], timeAgo[i].text, media[i].text))
                i += 1
            except IndexError:
                break
        return news_list
    
    def _check_if_too_long(self, news: GoogleNews):
        return len(news.title) + len(news.link) > 1024