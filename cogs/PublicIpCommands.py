import discord
from discord.ext import commands
from UseCases.Ip.GetPublicIp import GetPublicIp
from Dependency import get_public_ip

class PublicIpCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, get_public_ip: GetPublicIp):
        self.bot = bot
        self.get_public_ip = get_public_ip
        super().__init__()

    @commands.slash_command(name="publicip", description="Fetch and display the public IP address.")
    @commands.is_owner()
    async def fetch_public_ip(self, interaction):
        """Fetch and display the public IP address."""
        public_ip = self.get_public_ip.execute()
        if public_ip:
            await interaction.response.send_message(f"The bot's ip: {public_ip}", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to fetch public IP address. Please try again later.", ephemeral=True)

def setup(bot):
    bot.add_cog(PublicIpCommands(bot, get_public_ip))