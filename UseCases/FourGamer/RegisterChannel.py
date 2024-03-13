from Repository.FourGamerNews.FourGamerNewsRepository import FourGamerNewsRepository

class RegisterChannel:
    def __init__(self, repository: FourGamerNewsRepository):
        self.repository = repository

    def execute(self, channel_id: str):
        channel = self.repository.get_text_channels()
        if channel_id in channel:
            raise ValueError('Channel already exists')
        self.repository.add_text_channel(channel_id)