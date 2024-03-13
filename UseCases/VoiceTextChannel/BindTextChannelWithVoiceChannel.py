import asyncio

from Repository.VoiceTextChannel.VoiceTextChannelRepository import VoiceTextChannelRepository

class BindTextChannelWithVoiceChannelOutputPort:
    async def set_text_channel_invisible_to_all_users(self, text_channel_id: str):
        raise NotImplementedError

class BindTextChannelWithVoiceChannel:
    def __init__(self, repository: VoiceTextChannelRepository, output_port: BindTextChannelWithVoiceChannelOutputPort=None):
        self.repository = repository
        self.output_port = output_port

    def execute(self, text_channel_id: str, voice_channel_id: str):
        if self.output_port is None:
            return
        
        text_channel_ids = self.repository.get_text_channel_ids_by_voice_channel_id(voice_channel_id)
        print(text_channel_ids)
        if text_channel_ids:
            if text_channel_id in text_channel_ids:
                raise ValueError('Relation already exists')
        
        self.repository.add_relation(text_channel_id, voice_channel_id)
        asyncio.ensure_future(self.output_port.set_text_channel_invisible_to_all_users(text_channel_id))