import discord
from discord import Interaction
from discord.ext import commands
from Utils.time import get_current_time

from UseCases.CentralWeatherAdministration import *
from Dependency import get_typhoons, get_recent_quakes, get_typhoon_image

class CentralWeatherAdministrationCommands(commands.Cog):

    def __init__(self, bot, get_recent_quakes: GetRecentQuakes, get_typhoons: GetTyphoons, get_typhoon_image: GetTyphoonImage) -> None:
        self.bot = bot
        self.get_recent_quakes = get_recent_quakes
        self.get_typhoons = get_typhoons
        self.get_typhoon_image = get_typhoon_image
        super().__init__()

    @commands.slash_command(name='quake', description='地震查詢指令，會回傳最近 5 筆')
    async def _quake(self, interaction):
        quakes = self.get_recent_quakes.execute()
        embed = discord.Embed(title='搜尋近 5 起地震資料',description=f'當前日期與時間: `{get_current_time().strftime("%Y")}年{get_current_time().strftime("%m")}月{get_current_time().strftime("%d")}日 {get_current_time().strftime("%A %H:%M")}`\n', color=0x9932CC)
        embed.set_author(name='中央氣象局 - 最近地震', url='https://www.cwb.gov.tw/V8/C/E/index.html', icon_url='https://i.imgur.com/2p7dkIM.png')
        cnt = 1
        for quake in quakes:
            magnitude = quake.magnitude
            depth = quake.depth
            location = quake.location
            level = quake.level
            time = quake.time
            alarmColor = ''
            if float(magnitude) >= 6.5 and int(level[0]) >= 6:
                alarmColor = '🟥 芮氏規模6.5以上，最大震度6級以上。'
            elif float(magnitude) >= 6 and int(level[0]) >= 5:
                alarmColor = '🟧 芮氏規模6以上，最大震度5級以上。'
            elif float(magnitude) >= 5.5 and int(level[0]) >= 4:
                alarmColor = '🟨 芮氏規模5.5以上，最大震度4級以上。'
            else:
                alarmColor = '🟩 不嚴重'

            detail = f'```diff\n'\
                + f'地點: {location}\n'\
                + f'\n'\
                + f'===地震資料====\n'\
                + f'- 地震規模: {magnitude}\n'\
                + f'- 地震強度: {level}\n'\
                + f'- 深度: {depth}\n'\
                + f'===============\n' \
                + f'+ 時間: {time}\n'\
                + f'```'
            inline = True
            if cnt == 1:
                inline = False
            embed.add_field(name=f'{cnt}. {alarmColor}', value=detail, inline=inline)
            cnt += 1

        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='typhoon', description='颱風查詢指令，會回傳目前的颱風或熱帶性低氣壓資料')
    async def _typhoon(self, interaction):
        await interaction.response.defer()
        typhoons = self.get_typhoons.execute()
        if len(typhoons) == 0:
            developer = await self.bot.fetch_user(254808247884709892)
            embed = discord.Embed(title=f'目前沒有颱風(^_^)/', description=f'不信你自己去看 \n'f'[交通部中央氣象局傳送門](https://www.cwa.gov.tw/V8/C/P/Typhoon/TY_NEWS.html)\n\n如果有錯請叫{developer.name}  :P')
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(title='搜尋颱風資料',description=f'當前日期與時間: `{get_current_time().strftime("%Y")}年{get_current_time().strftime("%m")}月{get_current_time().strftime("%d")}日 {get_current_time().strftime("%A %H:%M")}`\n', color=0x9932CC)
        embed.set_author(name='中央氣象局 - 颱風資訊', url='https://www.cwa.gov.tw/V8/C/P/Typhoon/TY_NEWS.html', icon_url='https://i.imgur.com/2p7dkIM.png')
        cnt = 1
        for typhoon in typhoons:
            name = typhoon.name
            detail = f'```diff\n'\
                + f'颱風名稱: {name}\n'\
                + f'```'
            inline = True
            if cnt == 1:
                inline = False
            embed.add_field(name=f'{cnt}. {name}', value=detail, inline=inline)
            cnt += 1

        await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(CentralWeatherAdministrationCommands(bot, get_recent_quakes, get_typhoons, get_typhoon_image))