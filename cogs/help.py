from discord.ext import commands
import discord
from config import GUILD  # ← GIUSTO ORA

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Mostra i comandi disponibili")
    @discord.app_commands.guilds(GUILD)
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Comandi disponibili",
            description=(
                "/info - Informazioni Bot\n"
                "/help - Mostra questo messaggio\n"
                "/ping - Verifica se il bot è online\n"
                "/player <nickname> - Mostra il profilo del giocatore\n"
                "/clan <tag> - Mostra info dettagliate della squadriglia"
            ),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
