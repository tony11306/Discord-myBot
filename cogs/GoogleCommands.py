from discord.ext import commands
from discord import Interaction
import discord

from UseCases.Google import *
from Dependency import google_news

class GoogleCommands(commands.Cog):
    def __init__(self, bot, get_news: GetNews) -> None:
        self.bot = bot
        self.get_news = get_news
        super().__init__()

    @commands.slash_command(name='news', description='Google搜尋指令')
    async def _news(self, interaction, keyword: str):
        news = self.get_news.execute(keyword)
        embed = discord.Embed(title='Google搜尋結果', description=f'搜尋關鍵字: {keyword}', color=0x0080ff)
        for index, item in enumerate(news):
            embed.add_field(name=f'{index+1}. {item.time}', value=f'> [{item.title}----{item.media}]({item.link})', inline=False)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(GoogleCommands(bot, google_news))