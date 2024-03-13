from typing import List
import requests
from bs4 import BeautifulSoup

from Utils import get_24hours_ago

class FourGamerNews:
    def __init__(self, title: str, article_url: str, description: str, image_url: str, author: str, date: str) -> None:
        self.title: str = title
        self.article_url: str = article_url
        self.description: str = description
        self.image_url: str = image_url
        self.author: str = author
        self.date: str = date

class GetNews:
    def __init__(self) -> None:
        pass

    def execute(self, url='https://www.4gamers.com.tw/news') -> List[FourGamerNews]:
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_list = soup.find_all('div')
        yesterday = get_24hours_ago().strftime('%Y-%m-%d')

        result: List[FourGamerNews] = []
        for article_data in articles_list:
            if article_data.find('h4') is None or article_data.find('time')['datetime'].split('T')[0] != yesterday:
                continue
            title = article_data.find('h4').text.replace(' ', '').replace('\n', '')
            article_url = article_data.find('h4').find('a')['href']
            description = article_data.find_all('div')[1].text.replace(' ', '').replace('\n', '')
            image_url = article_data.find_all('div')[0].find('img')['src']
            author = article_data.find('div', class_='author').text
            date = article_data.find('time').text

            news = FourGamerNews(title, article_url, description, image_url, author, date)
            result.append(news)
        return result
    
if __name__ == '__main__':
    news = GetNews().execute()