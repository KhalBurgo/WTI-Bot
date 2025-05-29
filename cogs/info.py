import discord
from discord.ext import commands
from discord import app_commands
import platform
import datetime
import time
import psutil
from config import GUILD

BOT_VERSION = "1.0.0"  # Imposta la versione del tuo bot
start_time = time.time()

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Mostra le informazioni sul bot")
    @app_commands.guilds(GUILD)
    async def info(self, interaction: discord.Interaction):
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)
        uptime = str(datetime.timedelta(seconds=uptime_seconds))

        embed = discord.Embed(
            title="📊 Informazioni sul Bot",
            color=discord.Color.blurple()
        )

        embed.add_field(name="🤖 Nome", value=self.bot.user.name, inline=True)
        embed.add_field(name="🆔 ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="💾 Versione Bot", value=BOT_VERSION, inline=False)
        embed.add_field(name="🐍 Versione Python", value=platform.python_version(), inline=True)
        embed.add_field(name="📦 discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="🌐 Server connessi", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="⏱️ Uptime", value=uptime, inline=True)

        # Usa psutil per memoria usata (opzionale)
        mem = psutil.Process().memory_info().rss / 1024 / 1024
        embed.add_field(name="🧠 Memoria usata", value=f"{mem:.2f} MB", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
