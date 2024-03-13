import threading
from datetime import datetime, timedelta
import time
from typing import List
import asyncio

from UseCases.FourGamer import GetNews, FourGamerNews
from Repository.FourGamerNews.FourGamerNewsRepository import FourGamerNewsRepository

class FourGamerNewsServiceOutputPort:
    def __init__(self):
        pass

    async def broadcast(self, news: FourGamerNews, channel_ids: List[str]):
        raise NotImplementedError

class FourGamerNewsService:
    '''
    I have not yet think about how to kill the thread.
    '''

    def __init__(self, get_news: GetNews, repository: FourGamerNewsRepository, four_gamer_news_service_output_port: FourGamerNewsServiceOutputPort=None) -> None:
        self.get_news = get_news
        self.four_gamer_news_service_output_port = four_gamer_news_service_output_port
        self.repository = repository
        self.thread = None

    async def run(self):
        if self.four_gamer_news_service_output_port is None:
            return
        
        while True:
            now = datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            if now >= midnight:
                # If it's already past midnight, wait until next midnight
                midnight += timedelta(days=1)
            wait_seconds = (midnight - now).total_seconds()
            await asyncio.sleep(wait_seconds)
            news_list = self.get_news.execute()
            text_channel_ids = self.repository.get_text_channels()
            for news in news_list:
                await self.four_gamer_news_service_output_port.broadcast(news, text_channel_ids)