import discord
from discord.ext import commands
from discord.commands import option
from datetime import datetime, timedelta
import asyncio

from UseCases.Remind import *
from Model.Remind import Remind
from Dependency import add_remind, get_remind_by_user_id, remove_remind, bind_remind_channel, unbind_remind_channel, notify_remind

class RemindCommands(commands.Cog, NotifyRemindOutputPort):

    def __init__(self, bot: commands.Bot, add_remind: AddRemind, get_remind_by_user_id: GetRemindByUserID, remove_remind: RemoveRemind, bind_remind_channel: BindRemindChannel, unbind_remind_channel: UnbindRemindChannel) -> None:
        self.bot = bot
        self.add_remind = add_remind
        self.get_remind_by_user_id = get_remind_by_user_id
        self.remove_remind = remove_remind
        self.notify_remind = notify_remind
        self.bind_remind_channel = bind_remind_channel
        self.unbind_remind_channel = unbind_remind_channel
        super().__init__()

    async def notify(self, remind: Remind, channel_id: str):
        print(f'Notify: {remind.title}')
        channel = self.bot.get_channel(int(channel_id))
        user = await self.bot.fetch_user(remind.user_id)
        message = await channel.send(user.mention)
        embed = discord.Embed(title=f'⏰提醒!', description=f'{user.mention}')
        embed.add_field(name='內容:', value=remind.title)
        await message.edit(embed=embed)

    @commands.slash_command(name='remind', description='設定提醒指令')
    @option(name='title', description='提醒內容', type=str, required=True)
    @option(name='month', description='幾月', type=int, required=True, min_value=1, max_value=12)
    @option(name='day', description='幾號', type=int, required=True, min_value=1, max_value=31)
    @option(name='hour', description='幾點', type=int, required=True, min_value=0, max_value=23)
    @option(name='minute', description='幾分', type=int, required=True, min_value=0, max_value=59)
    async def _remind(self, interaction, title: str, month: int, day: int, hour: int, minute: int):
        user_id = interaction.user.id
        time = datetime(datetime.now().year, month, day, hour, minute)
        add_remind_args = AddRemindArgs(title, time, user_id, interaction.guild_id)
        try:
            id = self.add_remind.execute(add_remind_args)
            await interaction.response.send_message(f'✅**已設定提醒 「{title}」**, 提醒編號: {id}', ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @commands.slash_command(name='remind_after', description='可以設定相對時間，例如: 3天後提醒')
    @option(name='title', description='提醒內容', type=str, required=True)
    @option(name='day', description='幾天後', type=int, required=False, min_value=0)
    @option(name='hour', description='幾小時後', type=int, required=False, min_value=0)
    @option(name='minute', description='幾分鐘後', type=int, required=False, min_value=0)
    async def _remind_after(self, interaction, title: str, day: int = 0, hour: int = 0, minute: int = 0):
        if day == 0 and hour == 0 and minute == 0:
            interaction.response.send_message('❌**請至少設定一個時間參數**', ephemeral=True)
            return
        user_id = interaction.user.id
        time = datetime.now() + timedelta(days=day, hours=hour, minutes=minute)
        add_remind_args = AddRemindArgs(title, time, user_id, interaction.guild_id)
        try:
            id = self.add_remind.execute(add_remind_args)
            await interaction.response.send_message(f'✅**已設定提醒 「{title}」**, 提醒編號: {id}', ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)


    @commands.slash_command(name='remove_remind', description='查詢提醒指令')
    @option(name='id', description='提醒編號', type=int, required=True)
    async def _remove_remind(self, interaction, id: int):
        user_id = interaction.user.id
        server_id = interaction.guild_id
        try:
            self.remove_remind.execute(str(id), str(server_id), str(user_id))
            await interaction.response.send_message(f'✅**已移除提醒**, 提醒編號: {id}', ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f'❌**{e}**', ephemeral=True)

    @commands.slash_command(name='get_remind', description='查詢提醒指令')
    async def _get_remind(self, interaction):
        user_id = interaction.user.id
        reminds = self.get_remind_by_user_id.execute(str(user_id))
        embed = discord.Embed(title='提醒列表', description=f'查詢者: {interaction.user.mention}', color=0x0080ff)
        for remind in reminds:
            embed.add_field(name=f'編號: {remind.id}', value=f'內容: {remind.title}\n時間: {remind.time}')
        await interaction.response.send_message(embed=embed)
    
    @commands.slash_command(name='bind_remind_channel', description='設定該頻道為提醒頻道')
    @commands.has_permissions(administrator=True)
    async def _bind_remind_channel(self, interaction):
        try:
            self.bind_remind_channel.execute(str(interaction.guild_id), str(interaction.channel_id))
            await interaction.response.send_message('✅**已設定為提醒頻道**', ephemeral=True)
        except ValueError as e:
            self.unbind_remind_channel.execute(str(interaction.guild_id))
            self.bind_remind_channel.execute(str(interaction.guild_id), str(interaction.channel_id))
            await interaction.response.send_message('✅**偵測到此伺服器已經設定過提醒頻道，已將原設定覆蓋**', ephemeral=True)
    
    @_bind_remind_channel.error
    async def _bind_remind_channel_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('❌**此指令需要管理員權限**', ephemeral=True)
        else:
            await interaction.response.send_message('❌**發生錯誤**', ephemeral=True)
    
    @commands.slash_command(name='unbind_remind_channel', description='解除該頻道為提醒頻道')
    @commands.has_permissions(administrator=True)
    async def _unbind_remind_channel(self, interaction):
        try:
            self.unbind_remind_channel.execute(str(interaction.guild_id))
            await interaction.response.send_message('✅**已解除提醒頻道**', ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message('❌**此伺服器並未設定提醒頻道**', ephemeral=True)
    
    @_unbind_remind_channel.error
    async def _unbind_remind_channel_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('❌**此指令需要管理員權限**', ephemeral=True)
        else:
            await interaction.response.send_message('❌**發生錯誤**', ephemeral=True)

def setup(bot):
    cog = RemindCommands(bot, add_remind, get_remind_by_user_id, remove_remind, bind_remind_channel, unbind_remind_channel)
    notify_remind.output_port = cog
    bot.add_cog(cog)
    loop = asyncio.get_event_loop()
    # wait until bot is ready
    loop.create_task(notify_remind.run())
