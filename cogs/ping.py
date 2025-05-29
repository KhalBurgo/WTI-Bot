from discord.ext import commands
import discord
from config import GUILD  # ← OK ORA

# IMPORTANTE: importa l'oggetto GUILD dal main
#from main import GUILD

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Risponde con Pong!")
    @discord.app_commands.guilds(GUILD)  # ← NECESSARIO PER LA SYNC GUILD-ONLY
    async def ping_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong!")

async def setup(bot):
    await bot.add_cog(Ping(bot))
