from discord.ext import commands
from discord import Intents
import os

from Config import *
from Utils import ConsoleTextColor, get_colored_string, get_current_time


def load_cog_files(bot: commands.Bot, current_file_path: str):
    if current_file_path.startswith('./'):
        current_file_path = current_file_path[2:]

    for file_name in os.listdir(current_file_path):
        file_abs_path = current_file_path + '/' + file_name
        if os.path.isdir(file_abs_path):
            load_cog_files(bot, file_abs_path)
        elif file_abs_path.endswith('.py'):
            bot.load_extension(file_abs_path[:-3].replace('/', '.'))
            print(file_abs_path[:-3].replace('/', '.'), 'loaded')


if __name__ == '__main__':
    bot = commands.Bot(intents=Intents.default())
    load_cog_files(bot, COGS_FILE_PATH)

    @bot.listen('on_message')
    async def log(message):
        time = get_colored_string(get_current_time().strftime("%c"), ConsoleTextColor.YELLOW)
        channelName = get_colored_string(str(message.channel), ConsoleTextColor.GREEN)
        authorName = get_colored_string(message.author.display_name, ConsoleTextColor.UNDERLINE)
        messageContent = get_colored_string(message.content, ConsoleTextColor.BLUE)
        print(f'{time} [{channelName}] {authorName}:{messageContent}')


    @bot.slash_command(name='load', description='[開發者指令]載入cog')
    @commands.is_owner()
    async def _load(interaction, extension: str):
        try:
            bot.load_extension(f'cogs.{extension}')
            await interaction.response.send_message(f'✅**Successfully loaded extension:"{extension}"**', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'❌**Error loading extension:"{extension}"**\n```{e}```', ephemeral=True)

    @bot.slash_command(name='unload', description='[開發者指令]卸載cog')
    @commands.is_owner()
    async def _unload(interaction, extension):
        try:
            if extension in ['RemindCommands', 'FourGamerNewsCommands']:
                await interaction.response.send_message(f'❌**Error unloading extension:"{extension}"**\n```{extension} is not unloadable```', ephemeral=True)
            bot.unload_extension(f'cogs.{extension}')
            await interaction.response.send_message(f'✅**Successfully unloaded extension:"{extension}"**', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'❌**Error unloading extension:"{extension}"**\n```{e}```', ephemeral=True)

    @bot.slash_command(name='reload', description='[開發者指令]重新載入cog')
    @commands.is_owner()
    async def _reload(interaction, extension):
        try:
            if extension in ['RemindCommands', 'FourGamerNewsCommands']:
                await interaction.response.send_message(f'❌**Error reloading extension:"{extension}"**\n```{extension} is not reloadable```', ephemeral=True)
            bot.unload_extension(f'cogs.{extension}')
            bot.load_extension(f'cogs.{extension}')
            await interaction.response.send_message(f'✅**Successfully reloaded extension:"{extension}"**', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'❌**Error reloading extension:"{extension}"**\n```{e}```', ephemeral=True)
    bot.run(TOKEN)

