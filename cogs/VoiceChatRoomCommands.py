import discord
from discord.ext import commands
from discord import Member, VoiceState, SlashCommandOptionType
from discord.commands import option


from UseCases.VoiceTextChannel import *
from Dependency import voice_text_channel, bind_text_channel_with_voice_channel, unbind_text_channel_with_voice_channel

class VoiceChatRoomCommands(commands.Cog, VoiceTextChannelOutputPort, BindTextChannelWithVoiceChannelOutputPort, UnbindTextChannelWithVoiceChannelOutputPort):
    
    def __init__(self, bot: commands.Bot, voice_text_channel: VoiceTextChannel, bind_text_channel_with_voice_channel: BindTextChannelWithVoiceChannel, unbind_text_channel_with_voice_channel: UnbindTextChannelWithVoiceChannel) -> None:
        self.bot = bot
        self.voice_text_channel = voice_text_channel
        self.bind_text_channel_with_voice_channel = bind_text_channel_with_voice_channel
        self.unbind_text_channel_with_voice_channel = unbind_text_channel_with_voice_channel
        super().__init__()

    async def set_text_channel_visible_to_user(self, text_channel_id: str, user_id: str):
        text_channel = await self.bot.fetch_channel(int(text_channel_id))
        user = await self.bot.fetch_user(int(user_id))
        await text_channel.set_permissions(user, read_messages=True)

    async def set_text_channel_invisible_to_user(self, text_channel_id: str, user_id: str):
        text_channel = await self.bot.fetch_channel(int(text_channel_id))
        user = await self.bot.fetch_user(int(user_id))
        await text_channel.set_permissions(user, read_messages=False)

    async def set_text_channel_invisible_to_all_users(self, text_channel_id: str):
        text_channel = await self.bot.fetch_channel(int(text_channel_id))
        await text_channel.set_permissions(text_channel.guild.default_role, read_messages=False)

    async def set_text_channel_to_default(self, text_channel_id: str):
        text_channel = await self.bot.fetch_channel(int(text_channel_id))
        await text_channel.set_permissions(text_channel.guild.default_role, read_messages=True)
    
    @commands.Cog.listener(name='on_voice_state_update')
    async def update_voice_state(self, member: Member, before: VoiceState, after: VoiceState):
        
        # if the member is itself
        if member == self.bot.user:
            return

        if after.channel == before.channel: # User mute or deafen
            return
        if after.channel is not None and before.channel is not None: # User switch voice channel
            self.voice_text_channel.on_user_leave_voice_channel(str(member.id), str(before.channel.id))
            self.voice_text_channel.on_user_join_voice_channel(str(member.id), str(after.channel.id))
        elif after.channel is None: # User left voice channel
            self.voice_text_channel.on_user_leave_voice_channel(str(member.id), str(before.channel.id))
        else: # User joined voice channel
            self.voice_text_channel.on_user_join_voice_channel(str(member.id), str(after.channel.id))

    @commands.slash_command(name='bind_text_and_voice_channel', description='綁定文字頻道與語音頻道，當加入語音頻道時，文字頻道會自動顯示給該使用者')
    @commands.has_permissions(administrator=True)
    @option(name='text_channel', description='文字頻道', type=SlashCommandOptionType.channel, required=True)
    @option(name='voice_channel', description='語音頻道', type=SlashCommandOptionType.channel, required=True)
    async def bind_text_and_voice_channel(self, interaction, text_channel: discord.TextChannel, voice_channel: discord.VoiceChannel):
        try:
            self.bind_text_channel_with_voice_channel.execute(str(text_channel.id), str(voice_channel.id))
            await interaction.response.send_message(f'✅**已綁定文字頻道與語音頻道，請確保機器人可以存取該頻道，否則功能會異常**', ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @bind_text_and_voice_channel.error
    async def bind_text_and_voice_channel_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('❌**此指令需要管理員權限**', ephemeral=True)
        else:
            await interaction.response.send_message('❌**發生錯誤**', ephemeral=True)

    @commands.slash_command(name='unbind_text_and_voice_channel', description='解除綁定文字頻道與語音頻道')
    @commands.has_permissions(administrator=True)
    @option(name='text_channel', description='文字頻道', type=SlashCommandOptionType.channel, required=True)
    @option(name='voice_channel', description='語音頻道', type=SlashCommandOptionType.channel, required=True)
    async def unbind_text_and_voice_channel(self, interaction, text_channel: discord.TextChannel, voice_channel: discord.VoiceChannel):
        try:
            self.unbind_text_channel_with_voice_channel.execute(str(text_channel.id), str(voice_channel.id))
            await interaction.response.send_message(f'✅**已解除綁定文字頻道與語音頻道**', ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @unbind_text_and_voice_channel.error
    async def unbind_text_and_voice_channel_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('❌**此指令需要管理員權限**', ephemeral=True)
        else:
            await interaction.response.send_message('❌**發生錯誤**', ephemeral=True)

def setup(bot):
    cog = VoiceChatRoomCommands(bot, voice_text_channel, bind_text_channel_with_voice_channel, unbind_text_channel_with_voice_channel)
    bind_text_channel_with_voice_channel.output_port = cog
    unbind_text_channel_with_voice_channel.output_port = cog
    voice_text_channel.output_port = cog
    bot.add_cog(cog)