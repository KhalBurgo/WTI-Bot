from discord.ext import commands
import discord
import platform
import sys
from config import GUILD

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="info", description="Mostra informazioni sul bot")
    @discord.app_commands.guilds(GUILD)
    async def info_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📊 Info Bot",
            description="Ecco alcune informazioni sul bot:",
            color=discord.Color.blue()
        )

        embed.add_field(name="🤖 Nome bot", value=self.bot.user.name, inline=True)
        embed.add_field(name="🆔 ID bot", value=self.bot.user.id, inline=True)
        embed.add_field(name="🛠️ Versione Bot", value="1.0.0", inline=True)
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
        embed.add_field(name="📦 Libreria Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="💻 Sistema operativo", value=platform.system(), inline=True)
        embed.add_field(name="🧠 Autore", value="KhalBurgo", inline=True)
        embed.add_field(name="🔗 Server Discord", value="[War Thunder Italia](https://discord.gg/sfKvKuNwjh)", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
