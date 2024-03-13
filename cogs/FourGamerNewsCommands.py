import discord
from discord.ext import commands
from typing import List
import asyncio

from UseCases.FourGamer import *
from Dependency import four_gamer_news_service, register_channel

class FourGamerNewsCommands(commands.Cog, FourGamerNewsServiceOutputPort):

    def __init__(self, bot, register_channel: RegisterChannel) -> None:
        self.bot = bot
        self.register_channel = register_channel
        super().__init__()

    async def broadcast(self, news: FourGamerNews, channel_ids: List[str]):
        for channel_id in channel_ids:
            channel = self.bot.get_channel(int(channel_id))
            description = '------------\n' + news.description + '\n------------'
            embed = discord.Embed(title=news.title, url=news.article_url, description=description, color=0x0080ff)
            embed.set_author(name='4Gamer', url='https://www.4gamers.com.tw/news', icon_url='https://i.imgur.com/iyMOgPR.png')
            embed.set_thumbnail(url=news.image_url)
            embed.add_field(name='作者', value=news.author, inline=True)
            embed.add_field(name='文章發布日期', value=news.date, inline=True)
            await channel.send(embed=embed)

    @commands.slash_command(name='register_as_4gamers_news_channel', description='註冊該頻道為4Gamer新聞頻道')
    @commands.has_permissions(administrator=True)
    async def register(self, interation):
        try:
            self.register_channel.execute(interation.channel_id)
            await interation.response.send_message('✅**已註冊為4Gamer新聞頻道**', ephemeral=True)
        except ValueError as e:
            await interation.response.send_message(f'❌**{e}**', ephemeral=True)

    @register.error
    async def register_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('❌**此指令需要管理員權限**', ephemeral=True)
        else:
            await interaction.response.send_message('❌**發生錯誤**', ephemeral=True)


def setup(bot):
    cog = FourGamerNewsCommands(bot, register_channel)
    four_gamer_news_service.four_gamer_news_service_output_port = cog
    bot.add_cog(cog)
    loop = asyncio.get_event_loop()
    loop.create_task(four_gamer_news_service.run())