import asyncio

from Repository.VoiceTextChannel.VoiceTextChannelRepository import VoiceTextChannelRepository

class UnbindTextChannelWithVoiceChannelOutputPort:
    async def set_text_channel_to_default(self, text_channel_id: str):
        raise NotImplementedError

class UnbindTextChannelWithVoiceChannel:
    def __init__(self, repository: VoiceTextChannelRepository, output_port: UnbindTextChannelWithVoiceChannelOutputPort=None):
        self.repository = repository
        self.output_port = output_port

    def execute(self, text_channel_id: str, voice_channel_id: str):
        if self.output_port is None:
            return
        
        text_channel_ids = self.repository.get_text_channel_ids_by_voice_channel_id(voice_channel_id)
        if text_channel_ids and text_channel_id not in text_channel_ids:
            raise ValueError('Relation does not exist')

        self.repository.remove_relation(text_channel_id, voice_channel_id)
        asyncio.ensure_future(self.output_port.set_text_channel_to_default(text_channel_id))