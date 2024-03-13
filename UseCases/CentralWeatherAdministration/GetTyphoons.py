from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Model.Typhoon import Typhoon

class GetTyphoons:
    def __init__(self):
        pass

    def execute(self) -> List[Typhoon]:
        url = 'https://www.cwa.gov.tw/V8/C/P/Typhoon/TY_NEWS.html'
        options = Options()
        options.headless = True

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')

        # check if there is no typhoon
        p = soup.find('p', class_='WarnContent')
        if p and p.text == '目前無發布颱風消息。':
            return []

        typhoons = soup.find('div', id='MyOverall').find_all('div', class_='panel panel-default')
        typhoon_list = []
        for typhoon in typhoons:
            title = typhoon.find('h4', class_='panel-title')
            type = title.find('span', class_='fa-red').text
            name = title.find('span', class_='fa-blue').text
            typhoon_list.append(Typhoon(name, type))

        return typhoon_list
    
if __name__ == '__main__':
    get_typhoons = GetTyphoons()
    typhoons = get_typhoons.execute()
    for typhoon in typhoons:
        print(typhoon.name, typhoon.type)