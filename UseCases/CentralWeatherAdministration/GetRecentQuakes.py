import requests
from bs4 import BeautifulSoup
from typing import List

class Quake:
    def __init__(self, location: str, magnitude: str, level: str, depth: str, time: str):
        self.location: str = location
        self.magnitude: str = magnitude
        self.level: str = level
        self.depth: str = depth
        self.time: str = time

    def __eq__(self, other):
        if not isinstance(other, Quake):
            return False
        return self.location == other.location and self.magnitude == other.magnitude and self.level == other.level and self.depth == other.depth and self.time == other.time

class GetRecentQuakes:
    def __init__(self):
        pass

    def execute(self) -> List[Quake]:
        quakeUrl = 'https://www.cwa.gov.tw/V8/C/E/MOD/EQ_ROW.html'
        response = requests.get(quakeUrl)
        soup = BeautifulSoup(response.text, 'html.parser')
        quakeList = soup.find_all('tr', {'class': 'eq-row'}, limit=5)

        quakes = []
        for quake in quakeList:
            quakeDatas = quake.find('ul').find_all('li')
            magnitude = quakeDatas[2].text.replace('地震規模', '')
            depth = quakeDatas[1].text.replace('深度', '')
            if len(quakeDatas[0].find_all('br')) > 1:
                location = list(quakeDatas[0].find_all('br')[1].next_siblings)[0].strip('()')
            else:
                location = list(quakeDatas[0].find_all('br')[0].next_siblings)[0].strip('()')
            level = quake.find('td', {'headers': 'maximum'}).text
            date = quake.find('span').text
            quakes.append(Quake(location, magnitude, level, depth, date))
        return quakes
