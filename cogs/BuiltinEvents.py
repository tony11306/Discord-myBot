from discord.ext import commands

from Config import BOT_STATUS, BOT_ACTIVITY


class BuiltinEvents(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot initialized.')
        await self.bot.change_presence(status=BOT_STATUS, activity=BOT_ACTIVITY)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        pass
    
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        """ Print error text if happened."""

        print(f'\n{error}\n')
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'> 此指令不允許在這頻道使用')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'> 參數錯誤 {error}')
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        pass

def setup(bot):
    bot.add_cog(BuiltinEvents(bot))