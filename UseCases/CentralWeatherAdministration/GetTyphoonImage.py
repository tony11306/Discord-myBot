import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class GetTyphoonImage:
    def __init__(self):
        pass

    def execute(self) -> str:
        url = 'https://www.cwa.gov.tw/V8/C/P/Typhoon/TY_NEWS.html'
        options = Options()
        options.headless = True

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        image = 'https://www.cwa.gov.tw' + soup.find('img', id='slideImage-1')['src']
        return image