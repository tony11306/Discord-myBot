import discord
from discord.ext import commands
from discord.commands import option
from discord.voice_client import VoiceClient
import asyncio
from typing import List

from UseCases.Music import *
from Model.Song import Song
from Dependency import play, pause, continue_playing, remove_song_by_index, get_current_song, clear_song_list, search_youtube_song, add_song, get_song_list

class MusicCommands(commands.Cog, PlayOutputPort, PauseOutputPort, ContinueOutputPort):
    def __init__(self, bot: commands.Bot, play: Play, pause: Pause, continue_playing: Continue, remove_song_by_index: RemoveSongByIndex, get_current_song: GetCurrentSong, clear_song_list: ClearSongList, search_youtube_song: SearchYoutubeSong, add_song: AddSong, get_song_list: GetSongList) -> None:
        self.bot = bot
        self.play_use_case = play
        self.pause_use_case = pause
        self.continue_use_case = continue_playing
        self.remove_song_by_index_use_case = remove_song_by_index
        self.get_current_song_use_case = get_current_song
        self.clear_song_list_use_case = clear_song_list
        self.search_youtube_song_use_case = search_youtube_song
        self.add_song_use_case = add_song
        self.get_song_list_use_case = get_song_list
        
        self.guild_channel_map = {}
        self.lock = asyncio.Lock()
        super().__init__()

    def play(self, server_id: str, song: Song):
        self.bot.loop.create_task(self.async_play(server_id, song))
        
    async def async_play(self, server_id: str, song: Song):
        def pop_current_and_get_next():
            self.remove_song_by_index_use_case.execute(server_id, 0)
            return self.get_current_song_use_case.execute(server_id)

        guild = await self.bot.fetch_guild(int(server_id))
        voice_client: VoiceClient = guild.voice_client
        
        async with self.lock:
            if song and song.audio_url is None and not voice_client.is_playing(): # if the song is not processed yet, process it(possibly a song in playlist)
                songs = await self.search_youtube_song_use_case.execute(song.requester_id, song.webpage_url)
                song = songs[0]
        embed = await self.get_playing_song_notify_embed(song, server_id)
        channel = await self.bot.fetch_channel(self.guild_channel_map[server_id])
        if voice_client is None:
            return
        if not voice_client.is_playing():
            if song is None:
                self.guild_channel_map.pop(server_id, None)
            else:
                voice_client.play(discord.FFmpegPCMAudio(song.audio_url, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}), 
                                after=lambda e: self.play(server_id, pop_current_and_get_next()))
                voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                voice_client.source.volume = 0.1

            
            await channel.send(embed=embed)

    def pause(self, server_id: str, song: Song):

        async def async_pause():
            guild = await self.bot.fetch_guild(int(server_id))
            voice_client: VoiceClient = guild.voice_client
            if voice_client is None:
                return
            if voice_client.is_playing():
                voice_client.pause()

        asyncio.create_task(async_pause())

    def continue_playing(self, server_id: str):
        async def async_continue():
            guild = await self.bot.fetch_guild(int(server_id))
            voice_client: VoiceClient = guild.voice_client
            if voice_client is None:
                return
            if voice_client.is_paused():
                voice_client.resume()
        
        asyncio.create_task(async_continue())

    @commands.slash_command(name='play', description='播放音樂')
    @commands.bot_has_permissions(connect=True, speak=True)
    @commands.guild_only()
    @option(name='song_name', description='歌曲名稱或是網址', type=str, required=True)
    async def _play(self, interaction, song_name: str):
        def get_embed(songs: List[Song]):
            if len(songs) == 1:
                song = songs[0]
                song_list_len = len(self.get_song_list_use_case.execute(str(interaction.guild_id)))
                embed = discord.Embed(title=f'➕ 歌曲點播', description=f'已加入播放清單: [{song.title}]({song.webpage_url})', color=0x0080ff)
                embed.set_thumbnail(url=song.thumbnail)
                embed.set_footer(text=f'點歌者: {interaction.user.name}', icon_url=interaction.user.display_avatar.url)
                embed.set_author(name=song.uploader)
                embed.add_field(name='歌曲長度', value=song.duration_in_minutes_notation(), inline=True)
                embed.add_field(name='播放清單長度', value=f'還有 {song_list_len-1} 首歌正在佇列', inline=True)
                return embed
            elif len(songs) > 1:
                embed = discord.Embed(title='➕ 歌曲點播', description=f'已加入 {len(songs)} 首歌至清單', color=0x0080ff)
                embed.set_footer(text=f'點歌者: {interaction.user.name}', icon_url=interaction.user.display_avatar.url)
                #embed.set_thumbnail(url=songs[0].thumbnail)
                for index, song in enumerate(songs):
                    if index >= 4:
                        embed.add_field(name=f'...等 {len(songs) - index} 首', value='...', inline=False)
                        break
                    embed.add_field(name=f'`{song.title}`', value=f'{song.duration_in_minutes_notation()}', inline=False)
                return embed
            else:
                return discord.Embed(title='➕ 歌曲點播', description='找不到歌曲', color=0xff0000)

        if interaction.guild.voice_client is None:
            if interaction.author.voice is None:
                await interaction.response.send_message('❌**你不在任何語音頻道中**', ephemeral=True)
                return
            voice_channel = interaction.author.voice.channel
            await voice_channel.connect()

        server_id = str(interaction.guild_id)
        await interaction.response.defer()
        try:
            songs = await self.search_youtube_song_use_case.execute(interaction.user.id, song_name)
            for index ,song in enumerate(songs):
                self.add_song_use_case.execute(server_id, song)
                if index == 0:
                    self.play_use_case.execute(server_id)

            if server_id not in self.guild_channel_map:
                self.guild_channel_map[server_id] = interaction.channel_id
            await interaction.followup.send(embed=get_embed(songs), ephemeral=False)
        except ValueError as e:
            await interaction.followup.send(f'❌**{e}**', ephemeral=True)

    @commands.slash_command(name='pause', description='暫停音樂')
    @commands.guild_only()
    async def _pause(self, interaction):
        server_id = str(interaction.guild_id)
        try:
            self.pause_use_case.execute(server_id)
            await interaction.response.send_message(f'⏸️**已暫停音樂**', ephemeral=False)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @commands.slash_command(name='continue', description='繼續播放音樂')
    @commands.guild_only()
    async def _continue(self, interaction):
        server_id = interaction.guild_id
        try:
            self.continue_use_case.execute(server_id)
            await interaction.response.send_message(f'▶️**已繼續播放音樂**', ephemeral=False)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @commands.slash_command(name='skip', description='跳過目前播放的歌曲')
    @commands.guild_only()
    async def _skip(self, interaction):
        server_id = str(interaction.guild_id)
        try:
            self.pause_use_case.execute(server_id)
            self.remove_song_by_index_use_case.execute(server_id, 0)
            await interaction.response.send_message(f'⏭️**已跳過目前播放的歌曲**', ephemeral=False)
            self.play_use_case.execute(server_id)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @commands.slash_command(name='get_song_list', description='查詢播放清單，預設顯示第一頁')
    @option(name='page', description='頁數', type=int, min_value=1, required=False)
    @commands.guild_only()
    async def _get_song_list(self, interaction, page: int=1):
        server_id = str(interaction.guild_id)
        song_list = self.get_song_list_use_case.execute(server_id, page)
        embed = discord.Embed(title='播放清單', description=f'查詢者: {interaction.user.mention}', color=0x0080ff)
        for index, song in enumerate(song_list):
            member = await self.bot.fetch_user(int(song.requester_id))
            index = (page-1)*10 + index
            embed.add_field(name=f'編號: {index} ⬅️ 正在播放' if index == 0 else f'編號: {index}', value=f'歌名: {song.title}\n點歌者: {member.name}', inline=False)
        embed.set_footer(text=f'第 {page} 頁')
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='clear_song_list', description='清空播放清單')
    @commands.guild_only()
    async def _clear_song_list(self, interaction):
        server_id = str(interaction.guild_id)
        self.pause_use_case.execute(server_id)
        self.clear_song_list_use_case.execute(server_id)
        self.play_use_case.execute(server_id)
        await interaction.response.send_message(f'✅**已清空播放清單**', ephemeral=False)

    @commands.slash_command(name='leave', description='離開語音頻道')
    @commands.guild_only()
    async def _leave(self, interaction):
        server_id = str(interaction.guild_id)
        await interaction.guild.voice_client.disconnect()
        self.clear_song_list_use_case.execute(server_id)
        await interaction.response.send_message(f'👋**已離開語音頻道**', ephemeral=False)
        self.guild_channel_map.pop(server_id, None)

    @commands.slash_command(name='remove_song', description='移除播放清單中的歌曲')
    @option(name='index', description='歌曲編號', type=int, required=True)
    @commands.guild_only()
    async def _remove_song(self, interaction, index: int):
        server_id = str(interaction.guild_id)
        try:
            song = None
            if index == 0:
                self.pause_use_case.execute(server_id)
                song = self.remove_song_by_index_use_case.execute(server_id, index)
                self.play_use_case.execute(server_id)
            else:
                song = self.remove_song_by_index_use_case.execute(server_id, index)

            await interaction.response.send_message(f'✅**已移除播放清單中的歌曲: `{song.title}`**', ephemeral=False)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @commands.Cog.listener(name='on_voice_state_update')
    async def leave_if_everyone_left(self, member, before, after):
        # if the bot is not in any voice channel, return
        if member.guild.voice_client is None:
            return

        if after.channel is None:
            if before.channel is not None:
                if len(before.channel.members) == 1:
                    await member.guild.voice_client.disconnect()
                    self.clear_song_list_use_case.execute(str(member.guild.id))

    async def get_playing_song_notify_embed(self, song: Song, server_id: str):
        song_list = self.get_song_list_use_case.execute(server_id)
        if song is None or len(song_list) == 0:
            embed = discord.Embed(title='🎵 播放通知', description='播放清單已播放完畢', color=0x0080ff)
            return embed
        
        embed = discord.Embed(title=f'🎵 播放通知', description=f'正在播放: [{song.title}]({song.webpage_url})', color=0x0080ff)
        embed.set_thumbnail(url=song.thumbnail)
        member = await self.bot.fetch_user(int(song.requester_id))
        embed.set_footer(text=f'點歌者: {member.name}', icon_url=member.display_avatar.url)
        embed.set_author(name=song.uploader)
        embed.add_field(name='歌曲長度', value=song.duration_in_minutes_notation(), inline=True)
        embed.add_field(name='播放清單長度', value=f'還有 {len(self.get_song_list_use_case.execute(server_id))-1} 首歌正在佇列', inline=True)
        return embed


def setup(bot):
    cog = MusicCommands(bot, play, pause, continue_playing, remove_song_by_index, get_current_song, clear_song_list, search_youtube_song, add_song, get_song_list)
    play.output_port = cog
    pause.output_port = cog
    continue_playing.output_port = cog
    bot.add_cog(cog)

    