import time
from datetime import datetime
import threading
import asyncio

from Model.Remind import Remind
from Repository.Remind.RemindRepository import RemindRepository

class NotifyRemindOutputPort:
    def __init__(self):
        pass

    async def notify(self, remind: Remind, channel_id: str):
        raise NotImplementedError

class NotifyRemind:
    def __init__(self, repository: RemindRepository, output_port: NotifyRemindOutputPort=None):
        self.output_port = output_port
        self.repository = repository
        self.close = False

    async def run(self):
        if self.output_port is None:
            return
        elif self.close:
            return
        
        while not self.close:
            reminds = self.repository.get_expired_reminds()
            for remind in reminds:
                print(remind.server_id, self.repository.get_channel_id_by_server_id(remind.server_id))
                await self.output_port.notify(remind, self.repository.get_channel_id_by_server_id(remind.server_id))
                self.repository.remove(remind.id)
            wait_seconds = 60 - datetime.now().second
            await asyncio.sleep(wait_seconds + 1) # +1 for safety

    async def stop(self):
        self.close = True