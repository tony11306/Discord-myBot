import asyncio

from Repository.VoiceTextChannel.VoiceTextChannelRepository import VoiceTextChannelRepository

class VoiceTextChannelOutputPort:
    async def set_text_channel_visible_to_user(self, text_channel_id: str, user_id: str):
        raise NotImplementedError
    
    async def set_text_channel_invisible_to_user(self, text_channel_id: str, user_id: str):
        raise NotImplementedError

class VoiceTextChannel:
    def __init__(self, repository: VoiceTextChannelRepository, output_port: VoiceTextChannelOutputPort=None):
        self.output_port = output_port
        self.repository = repository
    
    def on_user_join_voice_channel(self, user_id: str, voice_channel_id: str):
        if self.output_port is None:
            return
        
        text_channel_id = self.repository.get_text_channel_ids_by_voice_channel_id(voice_channel_id)
        for channel_id in text_channel_id:
            asyncio.ensure_future(self.output_port.set_text_channel_visible_to_user(channel_id, user_id))


    def on_user_leave_voice_channel(self, user_id: str, voice_channel_id: str):
        if self.output_port is None:
            return
        
        text_channel_id = self.repository.get_text_channel_ids_by_voice_channel_id(voice_channel_id)
        for channel_id in text_channel_id:
            asyncio.ensure_future(self.output_port.set_text_channel_invisible_to_user(channel_id, user_id))
    

